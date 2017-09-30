using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Settings
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (maskedTextBox1.Text == "")
            {
                MessageBox.Show("You must fill in the field!");
            }
            else
            {
                try
                {
                    string str = string.Empty;
                    List<string> items = new List<string>();
                    using (System.IO.StreamReader reader = System.IO.File.OpenText(@"settings.txt"))
                    {
                        while (true)
                        {
                            str = reader.ReadLine();
                            if (str == null) break;
                            items.Add(str);
                        }
                    }
                    items[3] = maskedTextBox1.Text.Replace(" ", "").TrimStart('0');

                    using (System.IO.StreamWriter file = new System.IO.StreamWriter(@"settings.txt"))
                    {
                        foreach (string s in items)
                        {
                            file.WriteLine(s);
                        }
                    }
                    MessageBox.Show("Changes saved successfully!");
                    this.label1.Text = "Now maximal price is " + items[3].Replace(" ", "").TrimStart('0') + "$";
                }
                catch(Exception exc)
                {
                    this.label1.Text = "There are some problems. Your changes aren`t saved";
                }
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            try
            {
                string str = string.Empty;
                List<string> items = new List<string>();
                using (System.IO.StreamReader reader = System.IO.File.OpenText(@"settings.txt"))
                {
                    while (true)
                    {
                        str = reader.ReadLine();
                        if (str == null) break;
                        items.Add(str);
                    }
                }
                this.label1.Text = "Now maximal price is " + items[3].Replace(" ", "").TrimStart('0') + "$";
            }
            catch(Exception exc)
            {
                this.label1.Text = "Can`t read data from setting file";
            }
        }
    }
}
