Here is the complete scientific verification, parameter analysis, and implementation specification for your **AI-enabled multimodal wearable cognitive readiness system** during the 15-day Anulom-Vilom yoga study.

### 1\. Parameter Evidence Verification Table

Each parameter from your preliminary research claims has been verified against peer-reviewed literature, official Task Force guidelines, sensor technical documentation, and public dataset benchmarks 1-3.  
Parameter & Metric,Proposed Claim / Range,Verification Status,Unit,Gold Standard Measurement Protocol,Primary Source & Population,Key Limitations & Confounders,Engineering Recommendation  
HRV: RMSSD,\\\\(35 \\text{--} 65 \\text{ ms}\\\\),"Supported 2, 3",ms,"5-min resting seated PPG (or \\\\(60 \\text{ s}\\\\) ultra-short stationary recording) 2, 4.","Task Force (1996) 2, 3, Nunan et al. (2010) 2, 3, Healthy adults 18–22.","Sensitive to deep respiration, posture, recent physical exertion, and PPG motion artifacts 2, 4.","Primary parasympathetic vagal recovery index 2, 5\. Require complete stillness during 60s/5min window 4."  
HRV: SDNN,\\\\(40 \\text{--} 70 \\text{ ms}\\\\),"Supported 2, 3",ms,Standard 5-min baseline continuous PPG recording 2.,"Task Force (1996) 2, 3, Shaffer & Ginsberg (2017) 2.","Confounded by respiratory sinus arrhythmia (RSA) and short recording windows (\\\\(\<5\\text{ min}\\\\)) 2, 4.","Total autonomic variability index; do not derive from ultra-short (\\\\(\<5\\text{ min}\\\\)) windows 2, 4."  
Heart / Pulse Rate (HR/PR),\\\\(60 \\text{--} 80 \\text{ bpm}\\\\),"Supported 2, 6",bpm,PPG peak-to-peak interval detection at \\\\(\\ge 100\\text{ Hz}\\\\) sampling rate 4.,"Corsano / VitaStress Study (2025) 6, 7, Young adults (18–24).","Affected by anxiety, caffeine, digestion, ambient temperature, and motion 4, 6, 8.","Use as secondary cardiovascular demand check; filter out ectopic beats 4, 9."  
GSR/EDA: Tonic SCL,\\\\(2.0 \\text{--} 15.0 \\text{ }\\mu\\text{S}\\\\),"Supported 1, 3, 10",\\\\(\\mu\\text{S}\\\\),"Constant DC voltage (\\\\(0.5\\text{ V}\\\\)) across palmar/volar phalanges 10, 11.","Boucsein (2012) 3, 10, 12, iMotions Technical Guide 1, 10.","Massive inter-individual baseline variance due to skin hydration, temperature, and sweat gland density 10, 13.","Measure tonic sympathetic tone; normalize against individual resting baseline 13, 14."  
GSR/EDA: Phasic SCR Frequency,\\\\(1 \\text{--} 3 \\text{ peaks/min}\\\\) (resting),"Supported 1, 3, 10",peaks / min,"Trough-to-peak detection with threshold \\\\(\\ge 0.01 \\text{--} 0.02 \\text{ }\\mu\\text{S}\\\\) 10, 15.","Boucsein (2012) 3, 10, 12, iMotions Technical Guide 1, 15.","Reflects pure sympathetic arousal but contains no valence (cannot distinguish excitement/focus from distress) 5, 16, 17.","Index of acute sympathetic reactivity and cognitive engagement 1, 5."  
IMU Motion (\\\\(a\_{\\text{rms}}\\\\)),\\\\(\< 0.02 \\text{ g}\\\\) (Stationary gate),"Partially Supported / Engineering Rule 4, 18",g (\\\\(9.81 \\text{ m/s}^2\\\\)),"Tri-axial acceleration magnitude: \\\\(a\_{\\text{rms}} \= \\sqrt{a\_x^2+a\_y^2+a\_z^2} \- 1.0\\text{ g}\\\\) 18, 19.","van Hees et al. (2013) 18, Wearable PPG motion gating 4, 9.","Threshold depends heavily on mounting location (wrist vs. forearm) and sensor orientation 4, 18.","Gate PPG calculation when \\\\(a\_{\\text{rms}} \> 0.02\\text{--}0.03\\text{ g}\\\\) to prevent optical motion corruption 4, 9."  
1-Back Reaction Time (RT),\\\\(380 \\text{--} 520 \\text{ ms}\\\\),"Supported 3, 20",ms,"20–30 trial visual match/non-match task on touch display 2, 20.","Owen et al. (2005) 3, 20, Harvey et al. (2005) 20, Young adults.",Hardware/touch-screen display latency (\\\\(20 \\text{--} 50 \\text{ ms}\\\\)) must be subtracted; subject to practice effects 20.,"Measure executive processing speed; require touchscreen latency calibration 20, 21."  
1-Back Accuracy,\\\\(92\\% \\text{--} 98\\%\\\\),"Supported 3, 20",%,Proportion of correct target hits and non-target rejections 20.,"Owen et al. (2005) 3, 20, Healthy undergraduate cohorts.",High-performing engineering students exhibit ceiling effects on simple 1-back tasks 20.,"Measure executive attention maintenance; pair accuracy with RT 20, 22."

### 2\. Scientific Isolation Principles & Baseline Strategy

#### Why Single Sensors Cannot Establish Health or Readiness

* **GSR / EDA**: Pure sympathetic nervous system measure 5, 23\. An increase in SCL or SCR frequency indicates arousal intensity but carries no valence 16, 17\. High skin conductance occurs during acute stress, intense cognitive focus, physical exercise, or excitement 16, 24\.  
* **HRV (RMSSD/SDNN)**: Parasympathetic vagal tone index 2, 5\. Low HRV can stem from mental fatigue, acute distress, recent physical exertion, or caffeine intake 2, 4\.  
* **1-Back Task**: Measures working memory maintenance in the dorsolateral prefrontal cortex (dlPFC) 5\. Slow reaction time may reflect cognitive fatigue, boredom, or physical exhaustion 25\.  
* **Synthesis**: Cognitive readiness requires evaluating the **multimodal fusion** of parasympathetic recovery (HRV), sympathetic arousal (GSR), physical composure (IMU), and active cognitive performance relative to an individual's personal baseline 5, 22, 25\.

#### Defensible Personal Baseline Normalization (Rolling 5-Day Z-Score)

Due to substantial inter-individual differences in skin conductance, vascular tone, and cognitive baseline 10, 13, universal absolute cutoffs fail in real-world deployments 14\. A rolling 5-day Z-score provides a defensible normalization framework 14, 26:  
\\\\Z\_i \= \\frac{X\_{\\text{current}} \- \\bar{X}*{5\\text{-day}}}{\\sigma*{5\\text{-day}}}\\\\

* **Handling Low Variance (\\\\(\\sigma \\to 0\\\\))**: When a participant exhibits near-zero variance across baseline days, add a small regularization factor \\\\(\\epsilon \= 10^{-4}\\\\) or floor standard deviation at \\\\(\\sigma\_{\\text{min}} \= 0.05 \\cdot \\bar{X}\\\\) to prevent numerical instability.  
* **Handling Missing Data**: Apply forward-fill for contextual logs (sleep/caffeine) 9\. For sensor data, exclude corrupted windows rather than interpolating raw biosignals 9\. If IMU motion exceeds \\\\(0.02\\text{ g}\\\\), flag and invalidate that specific PPG window 4, 9\.

### 3\. Transparent Cognitive Readiness Index (CRI) Specification

The Cognitive Readiness Index (CRI) is a composite 0–100 score designed to fuse autonomic recovery, sympathetic arousal, physical stillness, and cognitive task performance 22, 27\.

#### CRI Mathematical Formula

\\\\\[\\text{CRI} \= \\text{Clip}\_{0}^{100} \\left( 50 \+ 10 \\times \\Bigw\_1 \\cdot Z\_{\\text{RMSSD}} \- w\_2 \\cdot Z\_{\\text{SCL}} \- w\_3 \\cdot Z\_{\\text{RT}} \+ w\_4 \\cdot Z\_{\\text{Acc}} \- w\_5 \\cdot Z\_{\\text{Fidget}} \\Big \\right)\\\\\]

#### Weight Distribution & Feature Directions

1. \\\\(w\_1 \= 0.25\\\\) (**RMSSD Z-Score**): Positive direction \\\\(+\\\\). Reflects parasympathetic vagal recovery and emotional flexibility 2, 5\.  
2. \\\\(w\_2 \= 0.20\\\\) (**Tonic SCL Z-Score**): Negative direction \\\\(-\\\\). Reflects excessive sympathetic over-arousal or stress load 1, 5\.  
3. \\\\(w\_3 \= 0.25\\\\) (**1-Back RT Z-Score**): Negative direction \\\\(-\\\\). Reflects cognitive slowing or mental fatigue 20, 22\.  
4. \\\\(w\_4 \= 0.20\\\\) (**1-Back Accuracy Z-Score**): Positive direction \\\\(+\\\\). Reflects executive attention and working memory accuracy 20, 22\.  
5. \\\\(w\_5 \= 0.10\\\\) (**IMU Fidgeting Z-Score**): Negative direction \\\\(-\\\\). Reflects physical restlessness and potential motion artifact risk 5, 19\.

\\\\\\sum\_{i=1}^{5} w\_i \= 0.25 \+ 0.20 \+ 0.25 \+ 0.20 \+ 0.10 \= 1.00\\\\

#### Experimental Readiness Bands

* **80 – 100 (Optimal Readiness)**: High vagal tone, low sympathetic stress, fast cognitive reaction time, high accuracy 27, 28\.  
* **60 – 79 (Moderate / Good Readiness)**: Nominal autonomic balance and stable working memory performance 27, 28\.  
* **40 – 59 (Sub-Optimal / Mild Fatigue)**: Elevated sympathetic arousal or sluggish reaction time; recovery recommended 27, 28\.  
* **0 – 39 (Low Readiness / Exhaustion)**: Vagal suppression, high SCL over-arousal, elevated 1-back errors; guided breathing/rest required 27, 28\.

*Missing Signal Fallback*: If PPG or GSR is motion-gated out, dynamically re-normalize weights \\\\(w\_i' \= \\frac{w\_i}{\\sum w\_{\\text{valid}}}\\\\) across available valid modalities 9\.

### 4\. Benchmark Comparison of Public Datasets

Dataset,Official URL / Access,Sensor Modalities & Hardware,Sampling Rates,Participant Cohort,Target Labels,Compatibility & Limitations for This Project  
WESAD,UCI ML Repository 29,"Empatica E4 Wrist (PPG, EDA, ACC, Temp) & RespiBAN Chest (ECG, EDA, EMG, ACC, Temp) 30.","Wrist PPG: \\\\(64\\text{ Hz}\\\\), EDA: \\\\(4\\text{ Hz}\\\\), ACC: \\\\(32\\text{ Hz}\\\\). Chest: \\\\(700\\text{ Hz}\\\\) 30.",15 subjects (young adults) 29.,"Neutral, TSST Stress, Amusement, Recovery 31.","Moderate Compatibility. Wrist PPG/EDA match hardware, but labels reflect acute social/cognitive laboratory stress rather than daily cognitive readiness or yoga recovery 32, 33."  
SWELL-KW,SWELL Dataset Portal 34,"Body sensors (ECG, EDA), Kinect facial/posture, computer interaction (keystrokes, mouse) 32, 35.","ECG: \\\\(2048\\text{ Hz}\\\\), EDA: \\\\(128\\text{ Hz}\\\\), Computer logs: Event-driven 32.",25 knowledge workers 32.,"Neutral, Time Pressure Stress, Interruption Stress 35.","High Conceptual Alignment for office/academic mental workload, but lacks PPG and arm/wrist IMU motion features 32."  
VitaStress,"VitaStress GitHub 36, 37","Corsano Cardiowatch 287-2B Wristband (PPG, EDA, 3-axis ACC, Temp, ECG) 7.","PPG/ACC: \\\\(32\\text{ Hz}/128\\text{ Hz}\\\\), EDA: \\\\(25\\text{ Hz}\\\\), Resampled to \\\\(0.33\\text{ Hz}\\\\) 7, 26.",21 subjects (mean age 24.1) 8.,"Neutral Baseline, Cognitive Stress (Mental Arithmetic), Socio-Evaluative Stress, Physical Exertion 38, 39.","Very High Alignment. Combines explicit cognitive stress (mental arithmetic) vs neutral baseline using wrist PPG/EDA/ACC 38, 40."  
*Critical Distinction*: Public stress datasets classify high-arousal threat/workload states 33, 40\. Cognitive readiness is a multi-dimensional state combining parasympathetic recovery (HRV), controlled arousal (GSR), and active executive task performance 5, 22\.

### 5\. Small-Data Machine Learning & Validation Strategy

#### Small Cohort Constraints (\\\\(N=4\\\\) participants, 15 days \= 60 sessions)

For a small feasibility cohort, complex deep neural networks or large random forests will severely overfit 41\.

#### Recommended Algorithmic Architecture

1. **Rule-Based Baseline**: Primary inference driven by the transparent CRI formula and threshold bounds 27, 41\.  
2. **Shallow CART Decision Tree**: Hyper-parameters set to max\_depth \= 3, min\_samples\_leaf \= 5, criterion \= 'gini' 41\.

                  \[ Z\_RMSSD \>= \-0.5 \]  
                         /        \\  
                       Yes         No  
                      /             \\  
       \[ Z\_SCL \< 0.8 \]               \[ Z\_RT \> 1.0 \]  
          /       \\                     /          \\  
      CLASS 1   CLASS 2             CLASS 3      CLASS 4  
     (Optimal   (Moderate           (Sub-Optimal (Low Readiness /  
    Readiness)  Readiness)          / Fatigued)   Exhausted)

#### Validation Scheme & Data Leakage Prevention

* **Participant-Wise Validation**: Utilize **Leave-One-Subject-Out Cross-Validation (LOSO-CV)** or GroupKFold(n\_splits=4) grouped strictly by Participant\_ID 9, 42\.  
* **Leakage Prevention**: Never perform random train/test splits across time-series samples from the same subject 9\. Normalize features strictly using statistics computed from the training fold 9\.  
* **Target Variables**: 3-Class readiness state (Optimal, Moderate, Low) derived from cluster labels or median-split cognitive performance paired with subjective ratings 27, 43\.  
* **Evaluation Metrics**: Macro F1-Score and Balanced Accuracy (robust against class imbalance) 9, 44\.  
* **Feasibility Boundary**: With \\\\(N=4\\\\), ML models evaluate system pipeline feasibility; results cannot claim statistically generalizable population accuracy 45, 46\. Synthetic data may test pipeline code execution but must never support claims of real-world model accuracy 45\.

### 6\. CSV Schema, Feature Pipeline & Coding Roadmap

#### Implementation-Ready CSV Data Schema (session\_features.csv)

participant\_id, day\_number, session\_mode (Pre\_Yoga / During\_Yoga / Post\_Yoga), timestamp, rmssd\_ms, sdnn\_ms, hr\_bpm, scl\_us, scr\_peaks\_per\_min, imu\_rms\_g, nback\_rt\_ms, nback\_accuracy\_pct, sleep\_hours, caffeine\_mg, stress\_self\_rating, cri\_score, readiness\_label 9, 27, 43\.

#### Feature Extraction Pipeline Specification

* **MAX30102 PPG**: Apply 2nd-order Butterworth bandpass filter (\\\\(0.5 \\text{--} 4.0 \\text{ Hz}\\\\)) 9, 47\. Detect inter-beat intervals (IBI) via peak detection (Pan-Tompkins or HeartPy). Compute \\\\(\\text{RMSSD} \= \\sqrt{\\frac{1}{N-1} \\sum (IBI\_{i+1} \- IBI\_i)^2}\\\\) and \\\\(\\text{SDNN} \= \\text{std}(IBI)\\\\) 2, 9\.  
* **GSR / EDA**: Apply 1 Hz lowpass filter to extract tonic SCL 9, 15\. Apply highpass filter (\\\\(0.05 \\text{ Hz}\\\\)) or trough-to-peak threshold (\\\\(\> 0.01 \\text{ }\\mu\\text{S}\\\\)) to count phasic SCR peak frequency per minute 9, 10, 15\.  
* **MPU6050 IMU**: Compute Signal Vector Magnitude \\\\(a\_{\\text{rms}} \= \\sqrt{a\_x^2 \+ a\_y^2 \+ a\_z^2} \- 1.0\\text{ g}\\\\) 18, 19\. Gate PPG processing if \\\\(a\_{\\text{rms}} \> 0.02\\text{ g}\\\\) 4, 9, 47\.

#### Prioritized Coding Roadmap

  Phase 1: Firmware & Sensor Stream (Day 1\)  
  ├── ESP32/Arduino Firmware: MAX30102 (100 Hz), GSR ADC (10 Hz), MPU6050 (50 Hz)  
  ├── BLE Packetizer: Synchronized raw binary transmission to mobile receiver  
  └── Python Signal Ingestion: Pan-Tompkins PPG peak detector & IMU motion gate (\>0.02 g)

  Phase 2: App Battery & Baseline Pipeline (Day 2\)  
  ├── Mobile 1-Back Engine: 20-trial task logging RT (ms) & Accuracy (%)  
  ├── Contextual Log Interface: Sleep hours, caffeine intake, Likert stress/fatigue  
  └── Rolling Baseline Engine: 5-day Z-score transformer & CRI calculator (0-100)

  Phase 3: 15-Day Feasibility Execution & Model Training (Weeks 1–4)  
  ├── Mode A Protocol: Mode A (Pre/Post Days 1 & 15\) and daily morning in-situ logs  
  ├── LOSO-CV Benchmark: Shallow CART decision tree vs. CRI rule-based baseline  
  └── Export Model: Edge deployment of decision rules to mobile app  
🧘 Would you like to write a Python script to test the rolling Z-score calculation and CRI scoring logic on sample session data?  
