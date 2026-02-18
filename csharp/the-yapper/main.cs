using System;
using System.Collections.Generic;

class Magic8Ball
{
    static void Main()
    {
        Random random = new();

        Console.WriteLine("╔══════════════════════════════════╗");
        Console.WriteLine("║            THE YAPPER            ║");
        Console.WriteLine("╚══════════════════════════════════╝");
        Console.WriteLine();

        while (true)
        {
            Console.Write("I am The Yapper and I will talk to you about random shit\n");
            Console.Write("Let's talk (/help for more info): ");
            string? input = Console.ReadLine();

            if (input.Equals("/help", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nCommand list:");
                Console.WriteLine("/help - Show this help message\n");
                Console.WriteLine("/quit - Exit the program\n");
                Console.WriteLine("/philosophy - Spew out bullshit philosophy\n");
                Console.WriteLine("/saymyname - SAY MY NAME\n");
                Console.WriteLine("/joke - Tell a random joke\n");
                Console.WriteLine("just talk to me for anything\n");
                continue;
            }
            if (input.Equals("/quit", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nAight bye");
                break;
            }
            // --------------------
            // this is a joke, dont take seriously!!!
            if (input.Equals("seig", StringComparison.OrdinalIgnoreCase)
            || input.Equals("heil", StringComparison.OrdinalIgnoreCase)
            || input.Equals("SEIG", StringComparison.OrdinalIgnoreCase)
            || input.Equals("HEIL", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nHEIL! (joking ofc)\n");
                continue;
            }
            // this is a joke, dont take seriously!!!
            if (input.Equals("is it gay to like femboys?", StringComparison.OrdinalIgnoreCase)
            || input.Equals("is it gay to like femboys", StringComparison.OrdinalIgnoreCase)
            || input.Equals("Is it gay to like femboys", StringComparison.OrdinalIgnoreCase)
            || input.Equals("Is it gay to like femboys?", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nU like them bc they look like women, then no, \nbut if u like theb bc of their personality then yes, mr weirdo\n");
                continue;
            }
            // this is a joke, dont take seriously!!!
            if (input.Equals("\ndeus vult", StringComparison.OrdinalIgnoreCase)
            || input.Equals("\nDEUS VULT", StringComparison.OrdinalIgnoreCase)
            || input.Equals("\nDeus Vult", StringComparison.OrdinalIgnoreCase)
            || input.Equals("\ndeus vult!", StringComparison.OrdinalIgnoreCase)
            || input.Equals("\nDEUS VULT!", StringComparison.OrdinalIgnoreCase)
            || input.Equals("\nDeus Vult!", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\n DEUS VULT\n");
                continue;
            }
            // this is a joke, dont take seriously!!!
            // --------------------
            if (input.IsWhiteSpace() || string.IsNullOrEmpty(input))
            {
                Console.WriteLine("\nSAY MY NAME");
                continue;
            }

            Console.WriteLine("\nTHE IDIOT IS THINKING...");
            Console.WriteLine();
        }
    }
}
