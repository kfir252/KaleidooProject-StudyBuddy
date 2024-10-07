using Microsoft.Win32;
using Newtonsoft.Json.Linq;  // For JSON parsing
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.IO;

namespace StudyBuddyUI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private async Task<string> SendQueryToServerAsync(string query)
        {
            using (HttpClient client = new HttpClient())
            {
                // Specify the API endpoint URL
                string apiUrl = "http://127.0.0.1:5000/query";

                // Create the JSON payload
                var jsonPayload = $"{{\"query\": \"{query}\"}}";
                var content = new StringContent(jsonPayload, Encoding.UTF8, "application/json");

                // Send the POST request to the server
                HttpResponseMessage response = await client.PostAsync(apiUrl, content);

                // Ensure the request was successful
                response.EnsureSuccessStatusCode();

                // Read the JSON response as a string
                string jsonResponse = await response.Content.ReadAsStringAsync();

                // Parse the JSON response and extract the "response" field
                JObject json = JObject.Parse(jsonResponse);
                string extractedResponse = json["response"]?.ToString();

                return extractedResponse;
            }
        }

        private async void Button_Click(object sender, RoutedEventArgs e)
        {
            // Append the user's question to the chat box
            chat_box.Text = chat_box.Text + "\nYou: " + question_box.Text;

            // Send the query to the API and get the response
            try
            {
                string query = question_box.Text;
                string response = await SendQueryToServerAsync(query);

                // Append the server's response to the chat box
                chat_box.Text = chat_box.Text + "\nServer: " + response;
            }
            catch (Exception ex)
            {
                // In case of an error, show the error message
                chat_box.Text = chat_box.Text + "\nError: " + ex.Message;
            }

            // Clear the question input box after sending the query
            question_box.Text = string.Empty;
        }

        private async void UploadFile_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "All Files (*.*)|*.*";
            if (openFileDialog.ShowDialog() == true)
            {
                string selectedFilePath = openFileDialog.FileName;
                MessageBox.Show("File selected: " + selectedFilePath);

                try
                {
                    // Send file to the server via API
                    string response = await UploadFileToServerAsync(selectedFilePath);
                    MessageBox.Show("Upload Successful: " + response);
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Error uploading file: " + ex.Message);
                }
            }
        }

        private async Task<string> UploadFileToServerAsync(string filePath)
        {
            using (HttpClient client = new HttpClient())
            {
                // Specify the API endpoint URL here
                string apiUrl = "http://127.0.0.1:5000";

                using (MultipartFormDataContent form = new MultipartFormDataContent())
                {
                    // Read file bytes and add them to the form
                    byte[] fileBytes = File.ReadAllBytes(filePath);
                    var fileContent = new ByteArrayContent(fileBytes);
                    fileContent.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("application/octet-stream");

                    // Add file content to the form with a name 'file'
                    form.Add(fileContent, "file", System.IO.Path.GetFileName(filePath));

                    // Send the form data to the server
                    HttpResponseMessage response = await client.PostAsync(apiUrl, form);

                    // Ensure a successful status code (throws exception if not)
                    response.EnsureSuccessStatusCode();

                    // Read response content as string
                    return await response.Content.ReadAsStringAsync();
                }
            }
        }
    }
}
