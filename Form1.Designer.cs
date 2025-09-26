namespace ServerClient
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            label1 = new Label();
            label2 = new Label();
            label3 = new Label();
            label4 = new Label();
            btnGonder = new Button();
            txtMesajGiris = new TextBox();
            txtSohbetLog = new TextBox();
            SuspendLayout();
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(327, 10);
            label1.Name = "label1";
            label1.Size = new Size(56, 20);
            label1.TabIndex = 0;
            label1.Text = "İstemci";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(43, 65);
            label2.Name = "label2";
            label2.Size = new Size(94, 20);
            label2.TabIndex = 1;
            label2.Text = "Mesaj Giriniz";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(43, 135);
            label3.Name = "label3";
            label3.Size = new Size(58, 20);
            label3.TabIndex = 2;
            label3.Text = "Gönder";
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Location = new Point(43, 191);
            label4.Name = "label4";
            label4.Size = new Size(112, 20);
            label4.TabIndex = 3;
            label4.Text = "Sohbet Geçmişi";
            // 
            // btnGonder
            // 
            btnGonder.Location = new Point(256, 131);
            btnGonder.Name = "btnGonder";
            btnGonder.Size = new Size(94, 29);
            btnGonder.TabIndex = 4;
            btnGonder.Text = "button1";
            btnGonder.UseVisualStyleBackColor = true;
            btnGonder.Click += btnGonder_Click;
            // 
            // txtMesajGiris
            // 
            txtMesajGiris.Location = new Point(256, 65);
            txtMesajGiris.Name = "txtMesajGiris";
            txtMesajGiris.Size = new Size(512, 27);
            txtMesajGiris.TabIndex = 5;
            // 
            // txtSohbetLog
            // 
            txtSohbetLog.Location = new Point(256, 200);
            txtSohbetLog.Name = "txtSohbetLog";
            txtSohbetLog.Size = new Size(512, 27);
            txtSohbetLog.TabIndex = 6;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(txtSohbetLog);
            Controls.Add(txtMesajGiris);
            Controls.Add(btnGonder);
            Controls.Add(label4);
            Controls.Add(label3);
            Controls.Add(label2);
            Controls.Add(label1);
            Name = "Form1";
            Text = "Form1";
            Load += Form1_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label label1;
        private Label label2;
        private Label label3;
        private Label label4;
        private Button btnGonder;
        private TextBox txtMesajGiris;
        private TextBox txtSohbetLog;
    }
}
