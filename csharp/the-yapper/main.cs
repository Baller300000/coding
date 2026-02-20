namespace System;

using System.Collections.Generic;

class Magic8Ball
{
    private static readonly List<string> philosophy = new()
    {
       "The only true wisdom is in knowing you know nothing. - Socrates\n",
        "I think, therefore I am. - René Descartes\n",
        "The unexamined life is not worth living. - Socrates\n",
        "Happiness is not something ready made. It comes from your own actions. - Dalai Lama\n",
        "The only way to do great work is to love what you do. - Steve Jobs\n",
        "In the middle of difficulty lies opportunity. - Albert Einstein\n",
        "The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela\n",
        "Life is what happens when you're busy making other plans. - John Lennon\n",
        "The best way to predict the future is to invent it. - Alan Kay\n",
        "Do not go where the path may lead, go instead where there is no path and leave a trail. - Ralph Waldo Emerson\n",
        "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt\n",
        "The mind is everything. What you think you become. - Buddha\n",
        "The only thing I know is that I know nothing. - Socrates\n",
        "The greatest wealth is to live content with little. - Plato\n",
        "SAY MY NAME - Walter White\n",
        "You're goddman right - Walter White\n",
        "You like kissing bois dont you? You fucking furry weirdo - Boykisser :3\n",
    };
    private static readonly List<string> dadjokes = new()
    {
       "Why don't scientists trust atoms? Because they make up everything!\n",
        "Why did the scarecrow win an award? Because he was outstanding in his field!\n",
        "Why don't skeletons fight each other? They don't have the guts!\n",
        "What do you call fake spaghetti? An impasta!\n",
        "Why did the bicycle fall over? Because it was two-tired!\n",
        "What do you call cheese that isn't yours? Nacho cheese!\n",
        "Why did the tomato turn red? Because it saw the salad dressing!\n",
        "What do you call a bear with no teeth? A gummy bear!\n",
        "Why did the golfer bring two pairs of pants? In case he got a hole in one!\n",
        "What do you call a snowman with a six-pack? An abdominal snowman!\n",
        "Why did the math book look sad? Because it had too many problems!\n",
        "What do you call a fish that wears a crown? A king fish!\n",
        "Why did the chicken go to the seance? To talk to the other side!\n",
        "What do you call a dog that can do magic? A labracadabrador!\n",
        "Why did the coffee file a police report? It got mugged!\n",
    };
    private static readonly List<string> eviljokes = new()
    {
        "Where did little Timmy go when he got lost in a minefield? Everywhere.\n",
        "Why did the orphan get hit by a car? Because he was an orphan.\n",
        "Why did the serial killer go to therapy? To work on his issues.\n",
        "What do you call a group of cannibals who eat a clown? A laughing stock.\n",
        "Why did the psychopath break up with his girlfriend? Because she was too normal.\n",
        "What is the difference between a snowman and a snowwoman? Snowballs.\n",
        "Why did the necrophiliac break up with his girlfriend? Because she was already dead.\n",
        "What do you call a group of evil clowns? A circus of doom.\n",
        "Why did the serial killer go to the grocery store? To pick up some fresh victims.\n",
        "What do you call a group of evil scientists? A lab of horrors.\n",
        "Why did the cannibal break up with his girlfriend? Because she was too tasty.\n",
        "What do you call a group of evil lawyers? A bar of evil.\n",
        "Why did the psychopath go to the doctor? To get a check-up on his sanity.\n",
        "What do you call a group of evil politicians? A senate of corruption.\n",
        "Why did 9/11 happen? Because of the weight of YO MAMA.\n",
    };
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

            if (string.Equals("/help", input, StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nCommand list:");
                Console.WriteLine("/help - Show this help message\n");
                Console.WriteLine("/quit - Exit the program\n");
                Console.WriteLine("/philosophy - Spew out bullshit philosophy\n");
                Console.WriteLine("/saymyname - SAY MY NAME\n");
                Console.WriteLine("/jokes dad - get a dad joke\n");
                Console.WriteLine("/jokes evil - get an evil joke\n");
                Console.WriteLine("just talk to me for anything\n");
                continue;
            }
            if (!string.IsNullOrEmpty(input))
            {
                Console.WriteLine(input.Length);
            }

            if (string.Equals("/quit", input, StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nAight bye");
                break;
            }
            if (string.Equals("/saymyname", input, StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nWalt: You all know exactly who I am. Say my name.\nDeclan: Do it? I don't have a damn clue who the hell you are.\nWalt: Yeah, you do. I'm the cook. I'm the man who killed Gus Fring.\nDeclan: [pauses] Heisenberg.\nWalt: You're goddamn right.\n");
                continue;
            }
            if (string.Equals("/philosophy", input, StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\n" + philosophy[random.Next(0, philosophy.Count)] + "\n");
                continue;
            }
            if (string.Equals("/jokes dad", input, StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\n" + dadjokes[random.Next(0, dadjokes.Count)] + "\n");
                continue;
            }
            if (string.Equals("/jokes evil", input, StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\n" + eviljokes[random.Next(0, eviljokes.Count)] + "\n");
                continue;
            }
            if (string.Equals("/jokes", input, StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nHavent made that yet\n");
            }
            // --------------------
            // this is a joke, dont take seriously!!!
            if (string.Equals("seig", input, StringComparison.OrdinalIgnoreCase)
            || string.Equals("heil", input, StringComparison.OrdinalIgnoreCase)
            || string.Equals("SEIG", input, StringComparison.OrdinalIgnoreCase)
            || string.Equals("HEIL", input, StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nHEIL! (joking ofc)\n");
                continue;
            }
            // this is a joke, dont take seriously!!!
            if (string.Equals("is it gay to like femboys?", input, StringComparison.OrdinalIgnoreCase)
            || string.Equals("is it gay to like femboys", input, StringComparison.OrdinalIgnoreCase)
            || string.Equals("Is it gay to like femboys", input, StringComparison.OrdinalIgnoreCase)
            || string.Equals("Is it gay to like femboys?", input, StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\nU like them bc they look like women, then no, \nbut if u like theb bc of their personality then yes, mr weirdo\n");
                continue;
            }
            // this is a joke, dont take seriously!!!
            if (string.Equals("\ndeus vult", input, StringComparison.OrdinalIgnoreCase)
            || string.Equals("\nDEUS VULT", input, StringComparison.OrdinalIgnoreCase)
            || string.Equals("\nDeus Vult", input, StringComparison.OrdinalIgnoreCase)
            || string.Equals("\ndeus vult!", input, StringComparison.OrdinalIgnoreCase)
            || string.Equals("\nDEUS VULT!", input, StringComparison.OrdinalIgnoreCase)
            || string.Equals("\nDeus Vult!", input, StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("\n DEUS VULT\n");
                continue;
            }
            // this is a joke, dont take seriously!!!
            // --------------------

            Console.WriteLine("\nTalk to me... (I have nothing to say back tho)\n");
            Console.WriteLine();
        }
    }
}
