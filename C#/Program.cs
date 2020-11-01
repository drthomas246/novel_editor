using System.Diagnostics;

namespace ConsoleApp1
{
    class Program
    {
        static void Main(string[] args)
        {
            ProcessStartInfo pInfo = new ProcessStartInfo();
            pInfo.FileName = System.IO.Path.GetFullPath("./dist/python.exe");
            pInfo.Arguments = System.IO.Path.GetFullPath("./dist/novel_editor.py");
            pInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;
            Process.Start(pInfo);
        }
    }
}
