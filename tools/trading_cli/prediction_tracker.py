#!/usr/bin/env python3
"""
Prediction Accuracy Tracker CLI Tool
====================================

Track and analyze prediction accuracy for continuous improvement
V2 Compliant: ≤400 lines, focused prediction tracking
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta
from typing import Any

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


class PredictionTracker:
    """Track and analyze prediction accuracy"""

    def __init__(self, db_path: str = "predictions.db"):
        """Initialize prediction tracker"""
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database for tracking predictions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create predictions table
            cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                prediction_date TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                action TEXT NOT NULL,
                target_price REAL NOT NULL,
                confidence REAL NOT NULL,
                reasoning TEXT,
                actual_price REAL,
                accuracy_score REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
            )

            # Create accuracy summary table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS accuracy_summary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    total_predictions INTEGER DEFAULT 0,
                    correct_predictions INTEGER DEFAULT 0,
                    accuracy_percentage REAL DEFAULT 0.0,
                    avg_confidence REAL DEFAULT 0.0,
                    last_updated TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conn.commit()

    def record_prediction(
        self,
        symbol: str,
        agent_id: str,
        action: str,
        target_price: float,
        confidence: float,
        reasoning: str = "",
    ) -> int:
        """Record a new prediction"""
        with sqlite3.connect(self.db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO predictions (symbol, prediction_date, agent_id, action, target_price, confidence, reasoning)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                symbol,
                datetime.now().isoformat(),
                agent_id,
                action,
                target_price,
                confidence,
                reasoning,
            ),
        )

        prediction_id = cursor.lastrowid
        conn.commit()
        conn.close()

        print(f"📝 Recorded prediction #{prediction_id} for {agent_id}")
        return prediction_id

    def update_actual_price(self, prediction_id: int, actual_price: float):
        """Update prediction with actual price and calculate accuracy"""
        with sqlite3.connect(self.db_path) as conn:
        cursor = conn.cursor()

        # Get the prediction
        cursor.execute("SELECT * FROM predictions WHERE id = ?", (prediction_id,))
        prediction = cursor.fetchone()

        if not prediction:
            print(f"❌ Prediction #{prediction_id} not found")
            conn.close()
            return

        # Calculate accuracy score
        target_price = prediction[5]  # target_price column
        accuracy_score = self._calculate_accuracy_score(
            target_price, actual_price, prediction[4]
        )  # action column

        # Update prediction
        cursor.execute(
            """
            UPDATE predictions
            SET actual_price = ?, accuracy_score = ?
            WHERE id = ?
        """,
            (actual_price, accuracy_score, prediction_id),
        )

        # Update accuracy summary
        self._update_accuracy_summary(prediction[1], prediction[3], cursor)  # symbol, agent_id

        conn.commit()
        conn.close()

        print(
            f"✅ Updated prediction #{prediction_id} with actual price ${actual_price:.2f} (accuracy: {accuracy_score:.1%})"
        )

    def _calculate_accuracy_score(
        self, target_price: float, actual_price: float, action: str
    ) -> float:
        """Calculate accuracy score based on prediction type"""
        price_diff = abs(actual_price - target_price) / target_price

        if action.lower() in ["buy", "strong_buy"]:
            # For buy predictions, accuracy is based on how close we got to the target
            if actual_price >= target_price * 0.95:  # Within 5% of target
                return 1.0
            elif actual_price >= target_price * 0.90:  # Within 10% of target
                return 0.8
            elif actual_price >= target_price * 0.80:  # Within 20% of target
                return 0.6
            else:
                return 0.3
        elif action.lower() in ["sell", "strong_sell"]:
            # For sell predictions, accuracy is based on how close we got to the target
            if actual_price <= target_price * 1.05:  # Within 5% of target
                return 1.0
            elif actual_price <= target_price * 1.10:  # Within 10% of target
                return 0.8
            elif actual_price <= target_price * 1.20:  # Within 20% of target
                return 0.6
            else:
                return 0.3
        else:  # hold
            # For hold predictions, accuracy is based on price stability
            if price_diff < 0.05:  # Less than 5% change
                return 1.0
            elif price_diff < 0.10:  # Less than 10% change
                return 0.8
            elif price_diff < 0.20:  # Less than 20% change
                return 0.6
            else:
                return 0.3

    def _update_accuracy_summary(self, symbol: str, agent_id: str, cursor):
        """Update accuracy summary for an agent"""
        # Get current stats
        cursor.execute(
            """
            SELECT COUNT(*), AVG(accuracy_score), AVG(confidence)
            FROM predictions
            WHERE symbol = ? AND agent_id = ? AND actual_price IS NOT NULL
        """,
            (symbol, agent_id),
        )

        total, avg_accuracy, avg_confidence = cursor.fetchone()

        if total is None:
            total = 0
            avg_accuracy = 0.0
            avg_confidence = 0.0

        # Count correct predictions (accuracy > 0.6)
        cursor.execute(
            """
            SELECT COUNT(*) FROM predictions
            WHERE symbol = ? AND agent_id = ? AND actual_price IS NOT NULL AND accuracy_score > 0.6
        """,
            (symbol, agent_id),
        )

        correct = cursor.fetchone()[0]

        # Update or insert summary
        cursor.execute(
            """
            INSERT OR REPLACE INTO accuracy_summary
            (symbol, agent_id, total_predictions, correct_predictions, accuracy_percentage, avg_confidence, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                symbol,
                agent_id,
                total,
                correct,
                avg_accuracy,
                avg_confidence,
                datetime.now().isoformat(),
            ),
        )

    def get_agent_accuracy(self, symbol: str = "TSLA", agent_id: str = None) -> dict[str, Any]:
        """Get accuracy statistics for agents"""
        with sqlite3.connect(self.db_path) as conn:
        cursor = conn.cursor()

        if agent_id:
            # Get specific agent stats
            cursor.execute(
                """
                SELECT * FROM accuracy_summary
                WHERE symbol = ? AND agent_id = ?
            """,
                (symbol, agent_id),
            )

            result = cursor.fetchone()
            if result:
                return {
                    "agent_id": result[1],
                    "total_predictions": result[2],
                    "correct_predictions": result[3],
                    "accuracy_percentage": result[4],
                    "avg_confidence": result[5],
                    "last_updated": result[6],
                }
            else:
                return None
        else:
            # Get all agents stats
            cursor.execute(
                """
                SELECT * FROM accuracy_summary
                WHERE symbol = ?
                ORDER BY accuracy_percentage DESC
            """,
                (symbol,),
            )

            results = cursor.fetchall()
            agents = []

            for result in results:
                agents.append(
                    {
                        "agent_id": result[1],
                        "total_predictions": result[2],
                        "correct_predictions": result[3],
                        "accuracy_percentage": result[4],
                        "avg_confidence": result[5],
                        "last_updated": result[6],
                    }
                )

            return agents

        conn.close()

    def get_recent_predictions(self, symbol: str = "TSLA", days: int = 7) -> list[dict[str, Any]]:
        """Get recent predictions"""
        with sqlite3.connect(self.db_path) as conn:
        cursor = conn.cursor()

        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

        cursor.execute(
            """
            SELECT * FROM predictions
            WHERE symbol = ? AND prediction_date >= ?
            ORDER BY prediction_date DESC
        """,
            (symbol, cutoff_date),
        )

        results = cursor.fetchall()
        predictions = []

        for result in results:
            predictions.append(
                {
                    "id": result[0],
                    "symbol": result[1],
                    "prediction_date": result[2],
                    "agent_id": result[3],
                    "action": result[4],
                    "target_price": result[5],
                    "confidence": result[6],
                    "reasoning": result[7],
                    "actual_price": result[8],
                    "accuracy_score": result[9],
                    "created_at": result[10],
                }
            )

        conn.close()
        return predictions

    def display_accuracy_report(self, symbol: str = "TSLA"):
        """Display comprehensive accuracy report"""
        print(f"\n📊 PREDICTION ACCURACY REPORT: {symbol}")
        print("=" * 60)

        # Get agent accuracy stats
        agents = self.get_agent_accuracy(symbol)

        if not agents:
            print("❌ No accuracy data available")
            return

        print("\n🤖 AGENT ACCURACY RANKINGS:")
        for i, agent in enumerate(agents, 1):
            accuracy = agent["accuracy_percentage"]
            confidence = agent["avg_confidence"]
            total = agent["total_predictions"]
            correct = agent["correct_predictions"]

            # Accuracy indicator
            if accuracy >= 0.8:
                accuracy_icon = "🟢"
            elif accuracy >= 0.6:
                accuracy_icon = "🟡"
            else:
                accuracy_icon = "🔴"

            print(f"  {i}. {accuracy_icon} {agent['agent_id']}: {accuracy:.1%} accuracy")
            print(f"     Predictions: {correct}/{total} correct")
            print(f"     Avg Confidence: {confidence:.1%}")
            print(f"     Last Updated: {agent['last_updated']}")
            print()

        # Get recent predictions
        recent = self.get_recent_predictions(symbol, 7)

        if recent:
            print("\n📈 RECENT PREDICTIONS (Last 7 days):")
            for pred in recent[:10]:  # Show last 10
                status = (
                    "✅"
                    if pred["accuracy_score"] and pred["accuracy_score"] > 0.6
                    else "❌"
                    if pred["actual_price"]
                    else "⏳"
                )
                print(
                    f"  {status} {pred['agent_id']}: {pred['action'].upper()} → ${pred['target_price']:.2f}"
                )
                if pred["actual_price"]:
                    print(
                        f"     Actual: ${pred['actual_price']:.2f} (Accuracy: {pred['accuracy_score']:.1%})"
                    )
                else:
                    print("     Waiting for actual price...")

    def export_data(self, symbol: str = "TSLA", output_file: str = None):
        """Export prediction data to JSON"""
        if not output_file:
            output_file = f"prediction_data_{symbol}_{datetime.now().strftime('%Y%m%d')}.json"

        # Get all data
        agents = self.get_agent_accuracy(symbol)
        recent = self.get_recent_predictions(symbol, 30)

        export_data = {
            "symbol": symbol,
            "export_date": datetime.now().isoformat(),
            "agent_accuracy": agents,
            "recent_predictions": recent,
        }

        with open(output_file, "w") as f:
            json.dump(export_data, f, indent=2)

        print(f"💾 Data exported to {output_file}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Prediction Accuracy Tracker")
    parser.add_argument("--symbol", "-s", default="TSLA", help="Stock symbol to track")
    parser.add_argument("--agent", "-a", help="Specific agent to analyze")
    parser.add_argument("--report", action="store_true", help="Display accuracy report")
    parser.add_argument("--export", help="Export data to file")
    parser.add_argument("--record", action="store_true", help="Record a new prediction")
    parser.add_argument("--update", type=int, help="Update prediction with actual price")
    parser.add_argument("--actual-price", type=float, help="Actual price for update")

    args = parser.parse_args()

    # Create tracker
    tracker = PredictionTracker()

    if args.record:
        # Interactive prediction recording
        print("📝 Recording new prediction...")
        agent_id = input("Agent ID: ")
        action = input("Action (buy/sell/hold): ")
        target_price = float(input("Target price: "))
        confidence = float(input("Confidence (0-1): "))
        reasoning = input("Reasoning: ")

        prediction_id = tracker.record_prediction(
            args.symbol, agent_id, action, target_price, confidence, reasoning
        )
        print(f"✅ Prediction recorded with ID: {prediction_id}")

    elif args.update and args.actual_price:
        # Update prediction with actual price
        tracker.update_actual_price(args.update, args.actual_price)

    elif args.report:
        # Display accuracy report
        tracker.display_accuracy_report(args.symbol)

    elif args.export:
        # Export data
        tracker.export_data(args.symbol, args.export)

    else:
        # Default: show accuracy for specific agent or all agents
        if args.agent:
            accuracy = tracker.get_agent_accuracy(args.symbol, args.agent)
            if accuracy:
                print(f"\n📊 {args.agent} Accuracy:")
                print(f"  Total Predictions: {accuracy['total_predictions']}")
                print(f"  Correct Predictions: {accuracy['correct_predictions']}")
                print(f"  Accuracy: {accuracy['accuracy_percentage']:.1%}")
                print(f"  Avg Confidence: {accuracy['avg_confidence']:.1%}")
            else:
                print(f"❌ No data found for {args.agent}")
        else:
            # Show all agents
            tracker.display_accuracy_report(args.symbol)


if __name__ == "__main__":
    main()
