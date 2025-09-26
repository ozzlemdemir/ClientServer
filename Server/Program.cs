// Örnek sunucu kodu

using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

public class MyServer
{
    public static void Main()
    {
        TcpListener server = null;
        try
        {
            server = new TcpListener(IPAddress.Parse("127.0.0.1"), 8000);
            server.Start();
            Console.WriteLine("Sunucu başlatıldı ve bağlantı bekleniyor...");

            TcpClient client = server.AcceptTcpClient();
            Console.WriteLine("Bir istemci bağlandı!");

            NetworkStream stream = client.GetStream();
            byte[] buffer = new byte[256];
            int bytesRead;
            string message;

            // İstemciden gelen veriyi sürekli oku
            while ((bytesRead = stream.Read(buffer, 0, buffer.Length)) != 0)
            {
                string receivedMessage = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                Console.WriteLine($"Gelen mesaj: {receivedMessage}");

                // İstemciye yanıt gönder
            
                string responseMessage = $"Mesajını aldım: '{receivedMessage}'";
                message=Console.ReadLine();
                byte[] responseData = Encoding.UTF8.GetBytes(message);
                stream.Write(responseData, 0, responseData.Length);
                Console.WriteLine("İstemciye yanıt gönderildi.");
            }

            // Döngüden çıkıldığında bağlantıyı kapat
            client.Close();
        }
        catch (SocketException e)
        {
            Console.WriteLine($"SocketException: {e}");
        }
        finally
        {
            server.Stop();
        }
    }
}