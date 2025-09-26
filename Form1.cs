using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
namespace ServerClient
{
    public partial class Form1 : Form
    {
        private TcpClient client;
        private NetworkStream stream;
        public Form1()
        {
            InitializeComponent();
        }
        private void DisplayMessage(string message)
        {
            //sunucudan anl?k mesaj gelip gelmedi?ini kontrol etmek için
            if (this.txtSohbetLog.InvokeRequired)
            {

                this.txtSohbetLog.Invoke(new Action<string>(DisplayMessage), message);
            }
            else
            {    //mesaj? ekrana yazd?r
                txtSohbetLog.AppendText(message + Environment.NewLine);
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            //form yüklendi?inde client ba?lat
            Task.Run(() => StartClient());

        }
        private void StartClient()
        {//client ba?latma
            Int32 port = 8000;
            string serverIp = "127.0.0.1";

            try
            {
                client = new TcpClient(serverIp, port);
                stream = client.GetStream();
                DisplayMessage("Sunucuya ba?land?.");

                byte[] buffer = new byte[256];
                int bytesRead;

                //sunucudan gelen mesaj? oku
                while ((bytesRead = stream.Read(buffer, 0, buffer.Length)) != 0)
                {
                    string receivedResponse = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    DisplayMessage($"Sunucu: {receivedResponse}");
                }
            }
            catch (SocketException ex)
            {
                DisplayMessage($"Ba?lant? Hatas?: {ex.Message}");
            }
            finally
            {
                if (stream != null) stream.Close();
                if (client != null) client.Close();
            }

        }

        private void btnGonder_Click(object sender, EventArgs e)
        {
            string message = this.txtMesajGiris.Text;

            if (string.IsNullOrEmpty(message)) return;


            DisplayMessage($"Sen: {message}");


            Task.Run(() => SendMessage(message));


            this.txtMesajGiris.Clear();
        }
        private void SendMessage(string message)
        {
            try
            {
                if (stream == null || !client.Connected)
                {
                    DisplayMessage("Hata: Sunucuya ba?l? de?il veya ba?lant? kesildi.");
                    return;
                }
                //mesaj? byte dizisine çevir ve gönder
                byte[] data = Encoding.UTF8.GetBytes(message);
                stream.Write(data, 0, data.Length);
            }
            catch (Exception ex)
            {
                DisplayMessage($"Gönderme Hatas?: {ex.Message}");
            }
        }
    }
}
