using System;
using System.Collections.Generic;

class Magic8Ball
{
    private static readonly List<string> Responses = new()
    {
        // GOOD BOIS :3
        "do it and ill give you a cookie",
        "I dont care about details, FUCK YEAAHH",
        "sure bro why not",
        "BULLSHIT. Do it now",
        "If you dont do it ill decapitate you",
        "DO IT",
        "FUCK YES",
        "The council of fuck yeah will decide",
        "FLOOR IT",
        "HELL YEAH",
        
        // IDK
        "LET ME THINK IN FUCKING PEACE",
        "FUCK IM SUPPOSED TO KNOW",
        "NUH UH",
        "SHUT UP",
        "GO COMMIT DIE",
        
        // NOPE
        "Don't count on MY FUCKING ASS",
        "My reply is FUCK NO",
        "do that shit, il end you",
        "That would be FUCKING STUPID",
        "FUCK NO",
        "ABSOLUTELY FUCKING NOT",
        "DO THAT AND ILL TOUCH U"
    };

    static void Main()
    {
        Random random = new();

        Console.WriteLine("╔════════════════════════════════════╗");
        Console.WriteLine("║        ANGRY 8 BALL IDIOT          ║");
        Console.WriteLine("╚════════════════════════════════════╝");
        Console.WriteLine();

        while (true)
        {
            Console.Write("Ask a yes-or-no question\n(or type '/quit' to exit): ");
            string? input = Console.ReadLine();

            if (input.Equals("/quit", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nFUCK OFF");
                break;
            }
            // ----------
            // this is a joke, dont take seriously!!!!
            if (input.Equals("seig", StringComparison.OrdinalIgnoreCase)
            || input.Equals("heil", StringComparison.OrdinalIgnoreCase)
            || input.Equals("SEIG", StringComparison.OrdinalIgnoreCase)
            || input.Equals("HEIL", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nHEIL! (joking ofc)");
                continue;
            }
            if (input.Equals("is it gay to like femboys?", StringComparison.OrdinalIgnoreCase)
            || input.Equals("is it gay to like femboys", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nU like them bc they look like women, then no, \nbut if u like theb bc of their personality then yes, mr weirdo");
                continue;
            }
            // this is a joke, dont take seriously!!!!
            // ----------
            if (input.IsWhiteSpace() || string.IsNullOrEmpty(input))
            {
                Console.WriteLine("\nASK A QUESTION YOU FUCKING IDIOT");
                continue;
            }

            Console.WriteLine("\nThe Magic 8 Ball is thinking...");
            for (int i = 0; i < 5; i++)
            {
                System.Threading.Thread.Sleep(300);
                Console.Write(".");
            }
            Console.WriteLine();

            // Get random response
            string response = Responses[random.Next(Responses.Count)];
            Console.WriteLine($"\n {response} \n");
        }
    }
}
