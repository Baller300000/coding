using System;
using System.Collections.Generic;

class Magic8Ball
{
    private static readonly List<string> Responses = new()
    {
        // GOOD BOIS :3
        "I dont care about details, FUCK YEAAHH",
        "sure bro why not",
        "FUCK YES",
        "The council of fuck yeah will decide",
        "FLOOR IT",
        "HELL YEAH",
        
        // IDK
        "LET ME THINK IN FUCKING PEACE",
        "FUCK IM SUPPOSED TO KNOW",
        "SHUT UP",
        "GO COMMIT DIE",
        "DEUS VULT\nDEUS VULT\nDEUS VULT",

        // NOPE
        "My reply is FUCK NO",
        "That would be FUCKING STUPID",
        "FUCK NO",
        "ABSOLUTELY FUCKING NOT",
        "ILL TOUCH U"
    };

    static void Main()
    {
        Random random = new();

        Console.WriteLine("╔═══════════════════════════════════╗");
        Console.WriteLine("║        ANGRY 8 BALL IDIOT         ║");
        Console.WriteLine("╚═══════════════════════════════════╝");
        Console.WriteLine();

        while (true)
        {
            Console.Write("DEUS VULT");
            Console.Write("Ask a yes-or-no question\n(or type '/quit' to exit): ");
            string? input = Console.ReadLine();

            if (input.Equals("/quit", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nFUCK OFF");
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
                Console.WriteLine("\nASK A QUESTION YOU FUCKING IDIOT");
                continue;
            }

            Console.WriteLine("\nTHE IDIOT IS THINKING...");
            Console.WriteLine();
            // Get random response
            string response = Responses[random.Next(Responses.Count)];
            Console.WriteLine($"\n {response} \n");
        }
    }
}
