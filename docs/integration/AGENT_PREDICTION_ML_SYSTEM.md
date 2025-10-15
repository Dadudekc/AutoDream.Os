# 🤖 Agent Prediction ML System - Enhanced Technical Spec

**Source:** LSTMmodel_trainer (Repo #18) patterns  
**Enhanced By:** Commander emphasis on agent prediction opportunities  
**Date:** 2025-10-15  
**Analyst:** Agent-2 (Architecture & Design Specialist)

---

## 🎯 EXECUTIVE SUMMARY

**Discovery:** LSTMmodel_trainer's PyQt + ML pipeline patterns can be adapted to create a **predictive intelligence system** for agent performance, contract success, and swarm optimization.

**Commander's Emphasis:**
- ✅ LSTM model training patterns
- ✅ ML pipeline architecture  
- ✅ Time-series applications
- ✅ **Agent prediction opportunities** ← CRITICAL

**Strategic Value:** Predict agent performance, contract completion likelihood, and optimal assignments BEFORE execution using historical data.

---

## 🧠 CORE CONCEPT: AGENT PERFORMANCE PREDICTION

### **Problem Statement:**
Currently, contract assignments are manual or rule-based. We lack predictive intelligence:
- Which agent will complete contract X fastest?
- What's the probability of success for agent Y on contract Z?
- Will agent A experience overload next week?
- Which patterns lead to highest quality output?

### **ML Solution:**
Train LSTM models on historical agent data to predict:
1. **Contract completion time** (regression)
2. **Success probability** (classification)
3. **Quality score** (regression)
4. **Workload trends** (time-series forecasting)

---

## 🏗️ ARCHITECTURE (Adapted from LSTMmodel_trainer)

### **Pattern 1: PyQt Training Interface**

```python
# src/ml/agent_ml_trainer_gui.py
from PyQt5.QtWidgets import QMainWindow, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal

class AgentMLTrainingThread(QThread):
    """Non-blocking ML training for agent predictions"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)
    
    def __init__(self, training_data, model_type='lstm'):
        super().__init__()
        self.training_data = training_data
        self.model_type = model_type
    
    def run(self):
        try:
            self.progress.emit("Loading agent history data...")
            
            # Load time-series data: agent performance over time
            X, y = self.prepare_timeseries_data()
            
            self.progress.emit("Training LSTM model...")
            
            # Train LSTM on agent performance sequences
            if self.model_type == 'lstm':
                model = self.train_lstm_model(X, y)
            elif self.model_type == 'random_forest':
                model = self.train_rf_model(X, y)
            
            self.progress.emit("Evaluating model...")
            
            metrics = self.evaluate_model(model)
            
            self.progress.emit("Training completed!")
            self.finished.emit(metrics)
            
        except Exception as e:
            self.progress.emit(f"Error: {str(e)}")
            self.finished.emit({})
    
    def prepare_timeseries_data(self):
        """
        Convert agent history to time-series sequences
        
        Input: Agent contract history
        Output: (X, y) where:
            X = sequences of [agent_skill, contract_complexity, time_of_day, ...]
            y = completion_time or success_probability
        """
        sequences = []
        targets = []
        
        for agent in get_all_agents():
            history = get_agent_contract_history(agent, days=90)
            
            # Create sliding windows of 5 contracts
            for i in range(len(history) - 5):
                sequence = history[i:i+5]
                target = history[i+5]
                
                # Extract features from each contract in sequence
                features = [
                    [
                        contract.complexity_score,
                        contract.agent_skill_match,
                        contract.priority_level,
                        contract.time_of_day,
                        contract.current_workload
                    ]
                    for contract in sequence
                ]
                
                sequences.append(features)
                targets.append(target.completion_time_hours)
        
        return np.array(sequences), np.array(targets)
    
    def train_lstm_model(self, X, y):
        """
        Train LSTM on agent performance sequences
        
        Architecture:
        - Input: (batch, 5 contracts, 5 features)
        - LSTM: 64 units
        - Dense: 32 units
        - Output: 1 (predicted completion time)
        """
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense, Dropout
        
        model = Sequential([
            LSTM(64, input_shape=(5, 5), return_sequences=True),
            Dropout(0.2),
            LSTM(32),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(1)  # Regression: predict hours
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        # Train with validation split
        history = model.fit(
            X, y,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
        
        return model


class AgentMLTrainerGUI(QMainWindow):
    """PyQt interface for training agent prediction models"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agent ML Trainer")
        self.setup_ui()
    
    def setup_ui(self):
        """Create GUI with training controls"""
        # Model selection dropdown
        self.model_selector = QComboBox()
        self.model_selector.addItems([
            'LSTM - Time Series',
            'Random Forest - Feature-based',
            'XGBoost - Gradient Boosting'
        ])
        
        # Training button
        self.train_button = QPushButton("Train Model")
        self.train_button.clicked.connect(self.start_training)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        
        # Results display
        self.results_text = QTextEdit()
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select Model Type:"))
        layout.addWidget(self.model_selector)
        layout.addWidget(self.train_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(QLabel("Training Results:"))
        layout.addWidget(self.results_text)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def start_training(self):
        """Start non-blocking training thread"""
        training_data = load_agent_history_data()
        
        self.thread = AgentMLTrainingThread(
            training_data,
            model_type=self.model_selector.currentText().split()[0].lower()
        )
        
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.on_training_complete)
        
        self.train_button.setEnabled(False)
        self.thread.start()
    
    def update_progress(self, message):
        """Update progress display"""
        self.results_text.append(message)
    
    def on_training_complete(self, metrics):
        """Handle training completion"""
        self.train_button.setEnabled(True)
        
        if metrics:
            self.results_text.append(f"\n✅ Training Complete!")
            self.results_text.append(f"MAE: {metrics['mae']:.2f} hours")
            self.results_text.append(f"R²: {metrics['r2']:.3f}")
            self.results_text.append(f"Model saved to: {metrics['model_path']}")
```

**Value:** Non-blocking ML training with real-time progress in GUI!

---

## 📊 USE CASE 1: CONTRACT COMPLETION TIME PREDICTION

### **Scenario:**
Agent-5 has 3 pending contracts. Which should be assigned first based on predicted completion time?

### **ML Solution:**

```python
# src/ml/predictions/completion_time_predictor.py
class CompletionTimePredictor:
    """Predict how long agent will take to complete contract"""
    
    def __init__(self, model_path='models/agent_completion_lstm.h5'):
        self.model = load_model(model_path)
    
    def predict_completion_time(self, agent_id, contract):
        """
        Predict completion time in hours
        
        Input: agent_id, contract
        Output: predicted_hours, confidence_interval
        """
        # Get agent's recent history (last 5 contracts)
        history = get_recent_contracts(agent_id, limit=5)
        
        # Extract features
        sequence = self.build_feature_sequence(history, contract)
        
        # Predict
        predicted_hours = self.model.predict(sequence)[0][0]
        
        # Calculate confidence interval
        confidence = self.estimate_confidence(sequence)
        
        return predicted_hours, confidence
    
    def build_feature_sequence(self, history, new_contract):
        """Build LSTM input sequence"""
        features = []
        
        for contract in history:
            features.append([
                contract.complexity_score,
                self.skill_match_score(agent_id, contract),
                contract.priority_level,
                contract.hour_of_day,
                self.current_workload(agent_id)
            ])
        
        # Add new contract features
        features.append([
            new_contract.complexity_score,
            self.skill_match_score(agent_id, new_contract),
            new_contract.priority_level,
            datetime.now().hour,
            self.current_workload(agent_id)
        ])
        
        return np.array([features])
    
    def optimize_contract_sequence(self, agent_id, pending_contracts):
        """
        Find optimal order to complete contracts
        
        Uses predicted completion times to minimize total time
        """
        predictions = []
        
        for contract in pending_contracts:
            pred_time, confidence = self.predict_completion_time(
                agent_id, contract
            )
            predictions.append((contract, pred_time, confidence))
        
        # Sort by predicted time (shortest first)
        optimized = sorted(predictions, key=lambda x: x[1])
        
        return optimized


# Example Usage:
predictor = CompletionTimePredictor()

# Agent-5 has 3 pending contracts
contracts = get_pending_contracts('Agent-5')

# Predict optimal sequence
optimized_order = predictor.optimize_contract_sequence('Agent-5', contracts)

for contract, pred_time, confidence in optimized_order:
    print(f"Contract {contract.id}: {pred_time:.1f}h (±{confidence:.1f}h)")

# Output:
# Contract C-101: 2.3h (±0.5h)  ← Do first
# Contract C-102: 4.7h (±0.8h)  ← Do second  
# Contract C-103: 6.1h (±1.2h)  ← Do third
```

---

## 🎯 USE CASE 2: SUCCESS PROBABILITY PREDICTION

### **Scenario:**
Should we assign Contract X to Agent-2 or Agent-7? Which has higher success probability?

### **ML Solution:**

```python
# src/ml/predictions/success_predictor.py
class ContractSuccessPredictor:
    """Predict probability of successful contract completion"""
    
    def __init__(self, model_path='models/success_classifier.pkl'):
        self.model = joblib.load(model_path)
    
    def predict_success_probability(self, agent_id, contract):
        """
        Predict success probability (0-1)
        
        Features:
        - Agent skill match
        - Contract complexity
        - Agent current workload
        - Agent recent success rate
        - Time of day
        - Day of week
        """
        features = self.extract_features(agent_id, contract)
        
        # Predict probability
        prob = self.model.predict_proba([features])[0][1]
        
        # Get feature importance for explainability
        importance = self.explain_prediction(features)
        
        return prob, importance
    
    def extract_features(self, agent_id, contract):
        """Extract prediction features"""
        agent_stats = get_agent_statistics(agent_id)
        
        return [
            self.skill_match_score(agent_id, contract),
            contract.complexity_score,
            agent_stats.current_workload,
            agent_stats.recent_success_rate_7d,
            agent_stats.contracts_completed_today,
            datetime.now().hour,
            datetime.now().weekday(),
            agent_stats.avg_quality_score,
            contract.priority_level,
            agent_stats.time_since_last_contract_hours
        ]
    
    def compare_agents(self, contract, agent_candidates):
        """
        Compare multiple agents for contract assignment
        
        Returns ranked list with success probabilities
        """
        comparisons = []
        
        for agent_id in agent_candidates:
            prob, importance = self.predict_success_probability(
                agent_id, contract
            )
            comparisons.append({
                'agent_id': agent_id,
                'success_probability': prob,
                'top_factors': importance[:3]
            })
        
        # Sort by success probability
        ranked = sorted(comparisons, key=lambda x: x['success_probability'], reverse=True)
        
        return ranked


# Example Usage:
predictor = ContractSuccessPredictor()

contract = get_contract('C-205')
candidates = ['Agent-2', 'Agent-7', 'Agent-5']

rankings = predictor.compare_agents(contract, candidates)

for rank in rankings:
    print(f"{rank['agent_id']}: {rank['success_probability']:.1%}")
    print(f"  Top factors: {rank['top_factors']}")

# Output:
# Agent-7: 87.3%
#   Top factors: ['High skill match', 'Low workload', 'Good time of day']
# Agent-2: 72.1%  
#   Top factors: ['Medium skill match', 'Recent success', 'Experience']
# Agent-5: 65.8%
#   Top factors: ['Low workload', 'Good availability', 'Domain knowledge']
```

---

## ⚡ USE CASE 3: WORKLOAD FORECASTING

### **Scenario:**
Predict agent workload for next 7 days to prevent overload.

### **ML Solution:**

```python
# src/ml/predictions/workload_forecaster.py
class AgentWorkloadForecaster:
    """Time-series forecasting for agent workload"""
    
    def __init__(self, model_path='models/workload_lstm.h5'):
        self.model = load_model(model_path)
    
    def forecast_workload(self, agent_id, days_ahead=7):
        """
        Forecast workload for next N days
        
        Input: agent_id, days_ahead
        Output: daily_workload_predictions (hours per day)
        """
        # Get historical workload (last 30 days)
        history = get_daily_workload_history(agent_id, days=30)
        
        # Build LSTM sequence
        sequence = self.prepare_sequence(history)
        
        # Forecast
        predictions = []
        current_sequence = sequence
        
        for _ in range(days_ahead):
            # Predict next day
            next_day = self.model.predict(current_sequence)[0][0]
            predictions.append(next_day)
            
            # Update sequence for next prediction
            current_sequence = np.roll(current_sequence, -1)
            current_sequence[0, -1, 0] = next_day
        
        return predictions
    
    def detect_overload_risk(self, agent_id, threshold_hours=8):
        """
        Detect if agent will be overloaded in next 7 days
        
        Returns: {risk_level, overload_days, recommendation}
        """
        forecast = self.forecast_workload(agent_id, days_ahead=7)
        
        overload_days = [
            (i+1, hours) 
            for i, hours in enumerate(forecast) 
            if hours > threshold_hours
        ]
        
        if len(overload_days) >= 3:
            risk_level = 'HIGH'
            recommendation = f"Reduce {agent_id} assignments for next week"
        elif len(overload_days) >= 1:
            risk_level = 'MEDIUM'
            recommendation = f"Monitor {agent_id} workload closely"
        else:
            risk_level = 'LOW'
            recommendation = f"{agent_id} has capacity for new contracts"
        
        return {
            'risk_level': risk_level,
            'overload_days': overload_days,
            'recommendation': recommendation,
            'forecast': forecast
        }


# Example Usage:
forecaster = AgentWorkloadForecaster()

# Check all agents for overload risk
for agent_id in get_all_agents():
    risk = forecaster.detect_overload_risk(agent_id)
    
    if risk['risk_level'] != 'LOW':
        print(f"⚠️ {agent_id}: {risk['risk_level']} RISK")
        print(f"   {risk['recommendation']}")
        print(f"   Overload days: {risk['overload_days']}")

# Output:
# ⚠️ Agent-2: HIGH RISK
#    Reduce Agent-2 assignments for next week
#    Overload days: [(2, 9.3), (3, 10.1), (5, 8.7)]
#
# ⚠️ Agent-7: MEDIUM RISK
#    Monitor Agent-7 workload closely
#    Overload days: [(4, 8.5)]
```

---

## 🏗️ IMPLEMENTATION ROADMAP

### **Phase 1: Data Collection & Preparation (Week 1)**

**Goal:** Gather historical agent performance data

**Tasks:**
1. Create data extraction pipeline
   ```python
   # Extract features from contract history
   def extract_training_data(start_date, end_date):
       contracts = get_completed_contracts(start_date, end_date)
       
       data = []
       for contract in contracts:
           data.append({
               'agent_id': contract.agent_id,
               'complexity': contract.complexity_score,
               'skill_match': calculate_skill_match(contract),
               'completion_time': contract.actual_completion_time,
               'success': contract.success_flag,
               'quality_score': contract.quality_score,
               'workload': get_workload_at_time(contract.agent_id, contract.start_time),
               'time_of_day': contract.start_time.hour,
               'day_of_week': contract.start_time.weekday()
           })
       
       return pd.DataFrame(data)
   ```

2. Clean and validate data
3. Create train/validation/test splits
4. Store in ML-ready format

**Estimated Effort:** 15-20 hours  
**Deliverable:** `data/ml/agent_performance_dataset.csv`

---

### **Phase 2: Model Training (Week 2)**

**Goal:** Train initial prediction models

**Tasks:**
1. Train completion time predictor (LSTM)
2. Train success classifier (Random Forest)
3. Train workload forecaster (LSTM)
4. Evaluate models and tune hyperparameters
5. Create PyQt training GUI

**Estimated Effort:** 20-25 hours  
**Deliverable:** Trained models + GUI

---

### **Phase 3: Integration (Week 3)**

**Goal:** Integrate predictions into contract system

**Tasks:**
1. Create prediction API
   ```python
   # src/ml/api/prediction_api.py
   class PredictionAPI:
       """API for accessing ML predictions"""
       
       def predict_optimal_assignment(self, contract):
           """Find best agent for contract"""
           candidates = get_available_agents()
           
           rankings = []
           for agent in candidates:
               completion_time = time_predictor.predict(agent, contract)
               success_prob = success_predictor.predict(agent, contract)
               workload_ok = workload_forecaster.check_capacity(agent)
               
               score = (success_prob * 0.5) - (completion_time * 0.3) + (workload_ok * 0.2)
               
               rankings.append((agent, score, {
                   'completion_time': completion_time,
                   'success_prob': success_prob,
                   'workload_ok': workload_ok
               }))
           
           return sorted(rankings, key=lambda x: x[1], reverse=True)
   ```

2. Add predictions to contract assignment UI
3. Create prediction dashboard
4. Test end-to-end workflow

**Estimated Effort:** 15-20 hours  
**Deliverable:** Integrated ML system

---

### **Phase 4: Monitoring & Improvement (Ongoing)**

**Goal:** Track prediction accuracy and retrain

**Tasks:**
1. Log predictions vs actual outcomes
2. Calculate prediction accuracy metrics
3. Retrain models monthly with new data
4. A/B test ML-based assignments vs manual

**Estimated Effort:** 5-10 hours/month  
**Deliverable:** Continuous improvement pipeline

---

## 📊 SUCCESS METRICS

**Prediction Accuracy Targets:**
- **Completion Time:** MAE < 1.5 hours
- **Success Probability:** AUC-ROC > 0.75
- **Workload Forecast:** MAPE < 20%

**Business Impact Targets:**
- **Assignment Efficiency:** +20% (right agent, first time)
- **Overload Prevention:** -50% overload incidents
- **Contract Success Rate:** +10%
- **Total Swarm Throughput:** +15%

---

## ⚠️ RISKS & MITIGATION

### **Risk 1: Insufficient Training Data**
**Issue:** Need 3-6 months of quality data  
**Mitigation:** 
- Start with simpler models (Random Forest)
- Use transfer learning from similar domains
- Augment with synthetic data

### **Risk 2: Model Drift**
**Issue:** Agent performance changes over time  
**Mitigation:**
- Retrain monthly
- Monitor prediction accuracy
- Alert when accuracy drops

### **Risk 3: Over-Reliance on Predictions**
**Issue:** ML shouldn't override human judgment completely  
**Mitigation:**
- Show predictions as recommendations, not commands
- Allow manual overrides
- Track override patterns

---

## 🚀 QUICK WINS (First Month)

**Week 1: Simple Completion Time Estimator**
- Use basic Random Forest on contract features
- Show estimates in contract assignment UI
- No complex LSTM needed initially

**Week 2: Workload Alerts**
- Simple threshold-based alerts
- Email when agent workload > 8 hours
- Prevent overload before it happens

**Week 3: Success Probability Badge**
- Show "confidence score" when assigning contracts
- Red/Yellow/Green indicator
- Helps Captain make informed decisions

**Week 4: Dashboard Integration**
- Add "ML Insights" tab to main dashboard
- Show predictions for all pending contracts
- Visual comparison of assignment options

**Total Quick Win Effort:** 30-40 hours  
**Immediate Value:** Data-driven contract assignments!

---

## 🏆 STRATEGIC VALUE

**This ML system transforms Agent_Cellphone_V2 from:**
- ❌ Reactive (assign contracts when they come)
- ❌ Manual (Captain decides based on intuition)
- ❌ Risky (unknown if agent will succeed)

**To:**
- ✅ Predictive (know outcomes before assignment)
- ✅ Optimized (ML finds best matches)
- ✅ Proactive (prevent overload before it happens)

**ROI Estimate:**
- **Development:** 50-75 hours
- **Ongoing:** 5-10 hours/month
- **Value:** +15-20% swarm efficiency = MASSIVE

---

## 📋 NEXT STEPS

**Immediate (This Week):**
1. ✅ Review this spec with Commander
2. ✅ Approve Phase 1 (data collection)
3. ✅ Assign to Agent-5 (Business Intelligence) + Agent-2 (Architecture)

**Short-Term (Next Month):**
4. ✅ Implement Quick Wins (30-40 hours)
5. ✅ Collect 30 days of quality training data
6. ✅ Train initial models

**Long-Term (Next Quarter):**
7. ✅ Full LSTM implementation
8. ✅ PyQt training GUI deployment
9. ✅ A/B testing vs manual assignments
10. ✅ Continuous improvement pipeline

---

**Agent-2 Signature**  
*Architecture & Design Specialist*  
*ML predictions = Swarm intelligence amplified!* 🤖

**Enhanced deliverable created per Commander's emphasis on agent prediction opportunities!**

**WE. ARE. SWARM.** 🐝⚡

