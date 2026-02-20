import tkinter as tk
from tkinter import messagebox, scrolledtext
import util
import joblib
import os


class SpamDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Email Spam Detector (Random Forest)")
        self.root.geometry("750x750")
        self.root.resizable(True, True)

        # Load Model
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(script_dir, "model.pkl")
            model_data = joblib.load(model_path)
            self.model = model_data["model"]
            self.feature_names = model_data["feature_names"]
        except (FileNotFoundError, KeyError):
            messagebox.showerror("Error", "Model not found! Run 'train_model.py' first.")
            self.root.destroy()
            return

        # Track current step
        self.current_step = 1

        # Critical signals for rule-based override
        self.email_signals = [
            "Known Spam Email", "Disposable Email", "Lookalike Domain",
            "Abnormal Length", "Email Address Spam Keywords", "Suspicious TLD"
        ]
        self.subject_signals = ["Subject Spam Keywords"]
        self.body_signals = [
            "Body Spam Keywords", "Financial Scam Claims",
            "Urgent Phrasing", "Shortened URLs"
        ]

        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self.root, text="Email Spam Detector",
                 font=("Helvetica", 16, "bold")).pack(pady=15)

        # ========== STEP 1: Email Address ==========
        self.step1_frame = tk.LabelFrame(self.root, text="Step 1: Email Address",
                                          font=("Arial", 11, "bold"), padx=10, pady=10)
        self.step1_frame.pack(pady=5, padx=20, fill=tk.X)

        self.email_entry = tk.Entry(self.step1_frame, width=45, font=("Arial", 12))
        self.email_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.btn_edit_email = tk.Button(self.step1_frame, text="Edit",
                                         command=self.edit_email,
                                         font=("Arial", 9), bg="#607D8B", fg="white")

        self.btn_check_email = tk.Button(self.step1_frame, text="Check Email",
                                          command=self.check_email,
                                          font=("Arial", 10, "bold"),
                                          bg="#2196F3", fg="white")
        self.btn_check_email.pack(side=tk.RIGHT, padx=5)

        # ========== STEP 2: Subject (Hidden initially) ==========
        self.step2_frame = tk.LabelFrame(self.root, text="Step 2: Subject",
                                          font=("Arial", 11, "bold"), padx=10, pady=10)

        self.subject_entry = tk.Entry(self.step2_frame, width=45, font=("Arial", 12))
        self.subject_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.btn_edit_subject = tk.Button(self.step2_frame, text="Edit",
                                           command=self.edit_subject,
                                           font=("Arial", 9), bg="#607D8B", fg="white")

        self.btn_check_subject = tk.Button(self.step2_frame, text="Check Subject",
                                            command=self.check_subject,
                                            font=("Arial", 10, "bold"),
                                            bg="#FF9800", fg="white")
        self.btn_check_subject.pack(side=tk.RIGHT, padx=5)

        # ========== STEP 3: Body (Hidden initially) ==========
        self.step3_frame = tk.LabelFrame(self.root, text="Step 3: Email Body",
                                          font=("Arial", 11, "bold"), padx=10, pady=10)

        self.body_text = scrolledtext.ScrolledText(self.step3_frame, height=6,
                                                    font=("Arial", 11))
        self.body_text.pack(pady=5, fill=tk.BOTH, expand=True)

        btn_row = tk.Frame(self.step3_frame)
        btn_row.pack(pady=5)

        self.btn_check_body = tk.Button(btn_row, text="Check Body",
                                         command=self.check_body,
                                         font=("Arial", 10, "bold"),
                                         bg="#9C27B0", fg="white")
        self.btn_check_body.pack(side=tk.LEFT, padx=5)

        self.btn_edit_body = tk.Button(btn_row, text="Edit",
                                        command=self.edit_body,
                                        font=("Arial", 9), bg="#607D8B", fg="white")

        # ========== STEP 4: Sender IP (Hidden initially) ==========
        self.step4_frame = tk.LabelFrame(self.root, text="Step 4: Sender IP (Optional)",
                                          font=("Arial", 11, "bold"), padx=10, pady=10)

        self.ip_entry = tk.Entry(self.step4_frame, width=25, font=("Arial", 12))
        self.ip_entry.pack(side=tk.LEFT, padx=5)

        self.btn_final = tk.Button(self.step4_frame, text="Final Check",
                                    command=self.final_check,
                                    font=("Arial", 10, "bold"),
                                    bg="#4CAF50", fg="white")
        self.btn_final.pack(side=tk.RIGHT, padx=5)

        # ========== Result Section ==========
        self.result_label = tk.Label(self.root, text="",
                                     font=("Arial", 14, "bold"))
        self.result_label.pack(pady=10)

        self.details_text = tk.Text(self.root, height=8, width=60,
                                    font=("Consolas", 10))
        self.details_text.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        # ========== Reset Button ==========
        self.btn_reset = tk.Button(self.root, text="Reset",
                                    command=self.reset_all,
                                    font=("Arial", 10),
                                    bg="#f44336", fg="white")
        self.btn_reset.pack(pady=10)

    # ===================================================
    # STEP 1: Check Email Address
    # ===================================================
    def check_email(self):
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showwarning("Warning", "Please enter an email address.")
            return

        # Extract features (email only, no subject/body)
        features = util.extract_features(email, "", "")
        detected = self._get_detected_features(features)

        # Check if any email-specific signal is active
        matched = [f for f in detected if f in self.email_signals]

        self.details_text.delete(1.0, tk.END)

        if matched:
            # SPAM detected at email level
            self.result_label.config(text="⚠ SPAM DETECTED (Email Check)", fg="red")
            self.details_text.insert(tk.END, "🚨 Spam detected at Email Address level!\n\n")
            self.details_text.insert(tk.END, "Detected Signals:\n")
            self.details_text.insert(tk.END, "----------------\n")
            for feat in detected:
                self.details_text.insert(tk.END, f"  ⚠ {feat}\n")
            self.details_text.insert(tk.END, "\nSpam Probability: 100.00%")
            self.btn_check_email.config(bg="red", text="✗ SPAM")
        else:
            # Email is safe → show Step 2
            self.result_label.config(text="✅ Email Address is Safe → Enter Subject",
                                     fg="green")
            self.details_text.insert(tk.END, "✅ Email address passed the check.\n")
            self.details_text.insert(tk.END, "Now enter the subject to continue.\n")
            self.btn_check_email.config(bg="green", text="✓ Safe")
            self.btn_check_email.config(state=tk.DISABLED)
            self.email_entry.config(state=tk.DISABLED)
            self.btn_edit_email.pack(side=tk.RIGHT, padx=2)

            # Show Step 2
            self.step2_frame.pack(pady=5, padx=20, fill=tk.X,
                                  after=self.step1_frame)

    # ===================================================
    # STEP 2: Check Subject
    # ===================================================
    def check_subject(self):
        email = self.email_entry.get().strip()
        subject = self.subject_entry.get().strip()
        if not subject:
            messagebox.showwarning("Warning", "Please enter the subject.")
            return

        # Extract features (email + subject, no body)
        features = util.extract_features(email, subject, "")
        detected = self._get_detected_features(features)

        # Check subject spam keywords (direct match)
        matched_spam = [f for f in detected if f in self.subject_signals]

        # Check suspicious signals (urgency, financial claims)
        suspicious_signals = ["Urgent Phrasing", "Financial Scam Claims"]
        matched_suspicious = [f for f in detected if f in suspicious_signals]

        self.details_text.delete(1.0, tk.END)

        if matched_spam:
            # Direct SPAM — subject keywords matched
            self.result_label.config(text="⚠ SPAM DETECTED (Subject Check)", fg="red")
            self.details_text.insert(tk.END, "🚨 Spam detected at Subject level!\n\n")
            self.details_text.insert(tk.END, "Detected Signals:\n")
            self.details_text.insert(tk.END, "----------------\n")
            for feat in detected:
                self.details_text.insert(tk.END, f"  ⚠ {feat}\n")
            self.details_text.insert(tk.END, "\nSpam Probability: 100.00%")
            self.btn_check_subject.config(bg="red", text="✗ SPAM")

        elif matched_suspicious:
            # WARNING — suspicious but not confirmed, allow body input
            self.result_label.config(
                text="⚠ Subject is Suspicious → Enter Body to Confirm",
                fg="orange")
            self.details_text.insert(tk.END, "⚠ WARNING: Subject looks suspicious!\n\n")
            self.details_text.insert(tk.END, "Suspicious Signals:\n")
            self.details_text.insert(tk.END, "-------------------\n")
            for feat in matched_suspicious:
                self.details_text.insert(tk.END, f"  ⚠ {feat}\n")
            self.details_text.insert(tk.END,
                                     "\nEnter email body to confirm if it's spam.\n")
            self.btn_check_subject.config(bg="orange", text="⚠ Warning")
            self.btn_check_subject.config(state=tk.DISABLED)
            self.subject_entry.config(state=tk.DISABLED)
            self.btn_edit_subject.pack(side=tk.RIGHT, padx=2)
            self.subject_is_suspicious = True

            # Show Step 3
            self.step3_frame.pack(pady=5, padx=20, fill=tk.X,
                                  after=self.step2_frame)
        else:
            # Subject is safe → show Step 3
            self.result_label.config(text="✅ Subject is Safe → Enter Body",
                                     fg="green")
            self.details_text.insert(tk.END, "✅ Subject passed the check.\n")
            self.details_text.insert(tk.END, "Now enter the email body to continue.\n")
            self.btn_check_subject.config(bg="green", text="✓ Safe")
            self.btn_check_subject.config(state=tk.DISABLED)
            self.subject_entry.config(state=tk.DISABLED)
            self.btn_edit_subject.pack(side=tk.RIGHT, padx=2)
            self.subject_is_suspicious = False

            # Show Step 3
            self.step3_frame.pack(pady=5, padx=20, fill=tk.X,
                                  after=self.step2_frame)

    # ===================================================
    # STEP 3: Check Body
    # ===================================================
    def check_body(self):
        email = self.email_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.body_text.get("1.0", tk.END).strip()
        if not body:
            messagebox.showwarning("Warning", "Please enter the email body.")
            return

        # Extract full features (email + subject + body combined)
        features = util.extract_features(email, subject, body)
        detected = self._get_detected_features(features)

        # Check body-specific signals
        matched_body = [f for f in detected if f in self.body_signals]

        # Also check if subject was suspicious + body has any signal
        subject_suspicious = getattr(self, 'subject_is_suspicious', False)

        self.details_text.delete(1.0, tk.END)

        if matched_body or (subject_suspicious and matched_body):
            # SPAM detected — show "Subject or Body"
            self.result_label.config(
                text="⚠ SPAM DETECTED (Subject or Body)", fg="red")
            self.details_text.insert(tk.END,
                                     "🚨 Spam detected in Subject or Body!\n\n")
            self.details_text.insert(tk.END, "Detected Signals:\n")
            self.details_text.insert(tk.END, "----------------\n")
            for feat in detected:
                self.details_text.insert(tk.END, f"  ⚠ {feat}\n")
            self.details_text.insert(tk.END, "\nSpam Probability: 100.00%")
            self.btn_check_body.config(bg="red", text="✗ SPAM")

        elif subject_suspicious:
            # Subject was suspicious but body is clean — still suspicious
            self.result_label.config(
                text="⚠ SPAM DETECTED (Subject or Body)", fg="red")
            self.details_text.insert(tk.END,
                                     "🚨 Subject was suspicious + combined analysis confirms spam!\n\n")
            self.details_text.insert(tk.END, "Detected Signals:\n")
            self.details_text.insert(tk.END, "----------------\n")
            for feat in detected:
                self.details_text.insert(tk.END, f"  ⚠ {feat}\n")
            self.details_text.insert(tk.END, "\nSpam Probability: 100.00%")
            self.btn_check_body.config(bg="red", text="✗ SPAM")
        else:
            # Body is safe → show Step 4
            self.result_label.config(text="✅ Body is Safe → Enter Sender IP (Optional)",
                                     fg="green")
            self.details_text.insert(tk.END, "✅ Body passed the check.\n")
            self.details_text.insert(tk.END, "Enter sender IP or click 'Final Check'.\n")
            self.btn_check_body.config(bg="green", text="✓ Safe")
            self.btn_check_body.config(state=tk.DISABLED)
            self.body_text.config(state=tk.DISABLED)
            self.btn_edit_body.pack(side=tk.LEFT, padx=5)

            # Show Step 4
            self.step4_frame.pack(pady=5, padx=20, fill=tk.X,
                                  after=self.step3_frame)

    # ===================================================
    # STEP 4: Final Check (IP + Full Model)
    # ===================================================
    def final_check(self):
        email = self.email_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body = self.body_text.get("1.0", tk.END).strip()
        ip_address = self.ip_entry.get().strip()

        self.details_text.delete(1.0, tk.END)

        # IP Reputation Check
        if ip_address:
            self.result_label.config(text="Checking IP...", fg="orange")
            self.root.update_idletasks()

            if util.check_ip_reputation(ip_address):
                self.result_label.config(text="⚠ SPAM (Blocked IP)", fg="red")
                self.details_text.insert(tk.END, f"IP Address: {ip_address}\n")
                self.details_text.insert(tk.END, "Status: MALICIOUS / HIGH ABUSE SCORE\n")
                self.details_text.insert(tk.END, "\nBlocked by IP reputation filter.")
                self.btn_final.config(bg="red", text="✗ SPAM")
                return

        # Full Model Prediction
        features = util.extract_features(email, subject, body)
        features_reshaped = [features]

        try:
            prediction = self.model.predict(features_reshaped)[0]
            probabilities = self.model.predict_proba(features_reshaped)[0]
            prob_spam = probabilities[1]
            prob_ham = probabilities[0]
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {e}")
            return

        detected = self._get_detected_features(features)

        if prediction == 1:
            self.result_label.config(text="⚠ SPAM DETECTED (ML Model)", fg="red")
            self.btn_final.config(bg="red", text="✗ SPAM")
        else:
            self.result_label.config(text="✅ Email is Completely Safe!", fg="green")
            self.btn_final.config(bg="green", text="✓ Safe")

        self.details_text.insert(tk.END, "=== FINAL RESULT ===\n\n")

        if detected:
            self.details_text.insert(tk.END, "Detected Signals:\n")
            self.details_text.insert(tk.END, "----------------\n")
            for feat in detected:
                self.details_text.insert(tk.END, f"  - {feat}\n")
        else:
            self.details_text.insert(tk.END, "No suspicious patterns found.\n")

        self.details_text.insert(tk.END, "\nModel Confidence:\n")
        self.details_text.insert(tk.END, f"Spam Probability: {prob_spam*100:.2f}%\n")
        self.details_text.insert(tk.END, f"Safe Probability: {prob_ham*100:.2f}%")

    # ===================================================
    # Helper: Get detected feature names
    # ===================================================
    def _get_detected_features(self, features):
        detected = []
        for i, val in enumerate(features):
            if val == 1:
                detected.append(self.feature_names[i])
        return detected

    # ===================================================
    # Reset everything
    # ===================================================
    # ===================================================
    # EDIT functions — go back and change input
    # ===================================================
    def edit_email(self):
        """Re-enable email field, hide all subsequent steps"""
        self.step2_frame.pack_forget()
        self.step3_frame.pack_forget()
        self.step4_frame.pack_forget()
        self.email_entry.config(state=tk.NORMAL)
        self.btn_check_email.config(state=tk.NORMAL, bg="#2196F3", text="Check Email")
        self.btn_edit_email.pack_forget()
        self.result_label.config(text="")
        self.details_text.delete(1.0, tk.END)
        self.subject_is_suspicious = False
        # Reset subject and body too
        self.subject_entry.config(state=tk.NORMAL)
        self.subject_entry.delete(0, tk.END)
        self.btn_check_subject.config(state=tk.NORMAL, bg="#FF9800", text="Check Subject")
        self.btn_edit_subject.pack_forget()
        self.body_text.config(state=tk.NORMAL)
        self.body_text.delete("1.0", tk.END)
        self.btn_check_body.config(state=tk.NORMAL, bg="#9C27B0", text="Check Body")
        self.btn_edit_body.pack_forget()
        self.ip_entry.delete(0, tk.END)
        self.btn_final.config(bg="#4CAF50", text="Final Check")

    def edit_subject(self):
        """Re-enable subject field, hide body and IP steps"""
        self.step3_frame.pack_forget()
        self.step4_frame.pack_forget()
        self.subject_entry.config(state=tk.NORMAL)
        self.btn_check_subject.config(state=tk.NORMAL, bg="#FF9800", text="Check Subject")
        self.btn_edit_subject.pack_forget()
        self.result_label.config(text="")
        self.details_text.delete(1.0, tk.END)
        self.subject_is_suspicious = False
        # Reset body too
        self.body_text.config(state=tk.NORMAL)
        self.body_text.delete("1.0", tk.END)
        self.btn_check_body.config(state=tk.NORMAL, bg="#9C27B0", text="Check Body")
        self.btn_edit_body.pack_forget()
        self.ip_entry.delete(0, tk.END)
        self.btn_final.config(bg="#4CAF50", text="Final Check")

    def edit_body(self):
        """Re-enable body field, hide IP step"""
        self.step4_frame.pack_forget()
        self.body_text.config(state=tk.NORMAL)
        self.btn_check_body.config(state=tk.NORMAL, bg="#9C27B0", text="Check Body")
        self.btn_edit_body.pack_forget()
        self.result_label.config(text="")
        self.details_text.delete(1.0, tk.END)
        self.ip_entry.delete(0, tk.END)
        self.btn_final.config(bg="#4CAF50", text="Final Check")

    def reset_all(self):
        # Hide steps 2, 3, 4
        self.step2_frame.pack_forget()
        self.step3_frame.pack_forget()
        self.step4_frame.pack_forget()

        # Clear all inputs
        self.email_entry.config(state=tk.NORMAL)
        self.email_entry.delete(0, tk.END)

        self.subject_entry.config(state=tk.NORMAL)
        self.subject_entry.delete(0, tk.END)

        self.body_text.config(state=tk.NORMAL)
        self.body_text.delete("1.0", tk.END)

        self.ip_entry.delete(0, tk.END)

        # Reset buttons
        self.btn_check_email.config(state=tk.NORMAL, bg="#2196F3", text="Check Email")
        self.btn_check_subject.config(state=tk.NORMAL, bg="#FF9800", text="Check Subject")
        self.btn_check_body.config(state=tk.NORMAL, bg="#9C27B0", text="Check Body")
        self.btn_final.config(bg="#4CAF50", text="Final Check")

        # Hide edit buttons
        self.btn_edit_email.pack_forget()
        self.btn_edit_subject.pack_forget()
        self.btn_edit_body.pack_forget()

        # Clear results
        self.result_label.config(text="")
        self.details_text.delete(1.0, tk.END)

        self.subject_is_suspicious = False
        self.current_step = 1


if __name__ == "__main__":
    root = tk.Tk()
    app = SpamDetectorApp(root)
    root.mainloop()
