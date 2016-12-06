using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace recovery1
{
    class Program
    {
        static void Main(string[] args)
        {
            /*string path = System.IO.Directory.GetCurrentDirectory() + "\\recoveryText.txt";
            string text = System.IO.File.ReadAllText(path);
            System.Console.WriteLine("The config file path is "+path);
            System.Console.WriteLine("The text is " + text);
            int i = text.IndexOf(" ");
            string filename = text.Substring(0,i);
            string destPath = text.Substring(i);
            System.Console.WriteLine("The dest path is " + destPath);
            string sourcePath = System.IO.Directory.GetCurrentDirectory() + filename;
            System.Console.WriteLine("The source path is " + sourcePath);

            System.IO.File.Copy(sourcePath,destPath, true);*/

            string path = System.IO.Directory.GetCurrentDirectory() + "\\recoveryText.txt";
            string[] text = System.IO.File.ReadAllLines(path);
            System.Console.WriteLine("The config file path is " + path);
            System.Console.WriteLine("The text is " + text);
            bool didTransfer = false;
            string err = "";

            for (int i = 0; i < text.Length; i++)
            {
                try
                {

                    int j = text[i].IndexOf(" ");
                    string filename = text[i].Substring(0, j);
                    string destPath = text[i].Substring(j);
                    System.Console.WriteLine("The dest path is " + destPath);
                    string sourcePath = System.IO.Directory.GetCurrentDirectory() + filename;
                    System.Console.WriteLine("The source path is " + sourcePath);
                    System.IO.File.Copy(sourcePath, destPath, true);
                }catch(System.IO.IOException e)
                {
                    err = e.Message;
                }
                didTransfer = true;
            }
            
            if (didTransfer)
            {
                string successMsg = "Files copied sucessfully.";
                System.Console.WriteLine(successMsg);
                MessageBox.Show(successMsg);
            }
            else
            {
                string failMsg = "Not all files were not copied due to: " + err;
                System.Console.WriteLine(failMsg);
                MessageBox.Show(failMsg);

            }
        }
        
    }
}
