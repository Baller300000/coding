using System;
using System.Collections.Generic;

class Magic8Ball
{
    private static readonly List<string> Responses = new()
    {
        // Positive answers (10)
        "It is certain",
        "It is decidedly so",
        "Without a doubt",
        "Yes definitely",
        "You may rely on it",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
        "Yes",
        "Signs point to yes",
        
        // Non-committal answers (5)
        "Reply hazy, try again",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict now",
        "Concentrate and ask again",
        
        // Negative answers (5)
        "Don't count on it",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful"
    };

    static void Main()
    {
        Random random = new();

        Console.WriteLine("╔════════════════════════════════════╗");
        Console.WriteLine("║        MAGIC 8 BALL ORACLE         ║");
        Console.WriteLine("╚════════════════════════════════════╝");
        Console.WriteLine();

        while (true)
        {
            Console.Write("Ask a yes-or-no question (or type 'quit' to exit): ");
            string? input = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(input))
                continue;

            if (input.Equals("quit", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nThanks for consulting the Magic 8 Ball! Goodbye!");
                break;
            }

            if (!input.EndsWith('?'))
            {
                Console.WriteLine("Please ask a question (ending with ?)");
                Console.WriteLine();
                continue;
            }

            // Shaking animation
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
