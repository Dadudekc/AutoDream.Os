#!/usr/bin/env python3
"""
Forecast Display Component
=========================

Modular forecast display widget for Tesla Stock App
V2 Compliant: ≤200 lines, focused forecast display
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)


class ForecastDisplayWidget(QWidget):
    """Modular forecast display widget"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()

        # Title
        title = QLabel("AI Forecast Analysis")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #4169E1; margin: 10px;")
        layout.addWidget(title)

        # Forecast summary
        self.forecast_group = QGroupBox("Forecast Summary")
        self.forecast_group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4169E1;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """
        )

        forecast_layout = QGridLayout()

        # Prediction
        self.prediction_label = QLabel("Prediction: Analyzing...")
        self.prediction_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.prediction_label.setStyleSheet("color: #4169E1; padding: 5px;")
        forecast_layout.addWidget(self.prediction_label, 0, 0)

        # Confidence
        self.confidence_label = QLabel("Confidence: 0%")
        self.confidence_label.setFont(QFont("Arial", 12))
        self.confidence_label.setStyleSheet("padding: 5px;")
        forecast_layout.addWidget(self.confidence_label, 0, 1)

        # Target price
        self.target_label = QLabel("Target Price: $0.00")
        self.target_label.setFont(QFont("Arial", 12))
        self.target_label.setStyleSheet("padding: 5px;")
        forecast_layout.addWidget(self.target_label, 1, 0)

        # Time horizon
        self.horizon_label = QLabel("Time Horizon: 1 day")
        self.horizon_label.setFont(QFont("Arial", 12))
        self.horizon_label.setStyleSheet("padding: 5px;")
        forecast_layout.addWidget(self.horizon_label, 1, 1)

        self.forecast_group.setLayout(forecast_layout)
        layout.addWidget(self.forecast_group)

        # Confidence bar
        confidence_group = QGroupBox("Confidence Level")
        confidence_layout = QVBoxLayout()

        self.confidence_bar = QProgressBar()
        self.confidence_bar.setRange(0, 100)
        self.confidence_bar.setValue(0)
        self.confidence_bar.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid #4169E1;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #4169E1;
                border-radius: 3px;
            }
        """
        )
        confidence_layout.addWidget(self.confidence_bar)

        confidence_group.setLayout(confidence_layout)
        layout.addWidget(confidence_group)

        # Agent predictions
        self.agents_group = QGroupBox("Agent Predictions")
        self.agents_group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4169E1;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """
        )

        agents_layout = QVBoxLayout()

        # Agent prediction labels
        self.agent_labels = []
        for i in range(8):
            agent_label = QLabel(f"Agent {i+1}: Analyzing...")
            agent_label.setFont(QFont("Arial", 10))
            agent_label.setStyleSheet("padding: 2px; color: #666;")
            self.agent_labels.append(agent_label)
            agents_layout.addWidget(agent_label)

        self.agents_group.setLayout(agents_layout)
        layout.addWidget(self.agents_group)

        # Analysis status
        self.analysis_frame = QFrame()
        self.analysis_frame.setFrameStyle(QFrame.Box)
        self.analysis_frame.setStyleSheet(
            """
            QFrame {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: #f9f9f9;
                margin: 5px;
            }
        """
        )

        analysis_layout = QHBoxLayout()
        self.analysis_label = QLabel("Analysis: Ready")
        self.analysis_label.setStyleSheet("color: #666; padding: 5px;")
        analysis_layout.addWidget(self.analysis_label)

        self.analysis_frame.setLayout(analysis_layout)
        layout.addWidget(self.analysis_frame)

        self.setLayout(layout)

    def update_forecast(self, forecast_data):
        """Update forecast display"""
        if not forecast_data:
            return

        # Update prediction
        prediction = forecast_data.get("prediction", "Analyzing...")
        self.prediction_label.setText(f"Prediction: {prediction}")

        # Color code prediction
        if "BUY" in prediction.upper():
            self.prediction_label.setStyleSheet("color: #228B22; padding: 5px; font-weight: bold;")
        elif "SELL" in prediction.upper():
            self.prediction_label.setStyleSheet("color: #DC143C; padding: 5px; font-weight: bold;")
        else:
            self.prediction_label.setStyleSheet("color: #4169E1; padding: 5px; font-weight: bold;")

        # Update confidence
        confidence = forecast_data.get("confidence", 0)
        self.confidence_label.setText(f"Confidence: {confidence:.1f}%")
        self.confidence_bar.setValue(int(confidence))

        # Update target price
        target_price = forecast_data.get("target_price", 0)
        self.target_label.setText(f"Target Price: ${target_price:.2f}")

        # Update time horizon
        horizon = forecast_data.get("time_horizon", "1 day")
        self.horizon_label.setText(f"Time Horizon: {horizon}")

    def update_agent_predictions(self, agent_data):
        """Update agent predictions display"""
        if not agent_data:
            return

        for i, agent_pred in enumerate(agent_data[:8]):  # Limit to 8 agents
            if i < len(self.agent_labels):
                agent_name = agent_pred.get("agent", f"Agent {i+1}")
                prediction = agent_pred.get("prediction", "Analyzing...")
                confidence = agent_pred.get("confidence", 0)

                text = f"{agent_name}: {prediction} ({confidence:.1f}%)"
                self.agent_labels[i].setText(text)

                # Color code based on prediction
                if "BUY" in prediction.upper():
                    self.agent_labels[i].setStyleSheet(
                        "padding: 2px; color: #228B22; font-weight: bold;"
                    )
                elif "SELL" in prediction.upper():
                    self.agent_labels[i].setStyleSheet(
                        "padding: 2px; color: #DC143C; font-weight: bold;"
                    )
                else:
                    self.agent_labels[i].setStyleSheet("padding: 2px; color: #666;")

    def update_analysis_status(self, status):
        """Update analysis status"""
        self.analysis_label.setText(f"Analysis: {status}")

        if "Error" in status or "Failed" in status:
            self.analysis_label.setStyleSheet("color: #DC143C; padding: 5px; font-weight: bold;")
        elif "Complete" in status or "Success" in status:
            self.analysis_label.setStyleSheet("color: #228B22; padding: 5px; font-weight: bold;")
        else:
            self.analysis_label.setStyleSheet("color: #666; padding: 5px;")
