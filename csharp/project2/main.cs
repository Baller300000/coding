using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

namespace Tetris
{
    class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new TetrisForm());
        }
    }

    public class TetrisForm : Form
    {
        private Timer gameTimer;
        private Game game;
        private bool isPaused;
        private int highScore;
        private const string HighScoreFile = "highscore.txt";

        public TetrisForm()
        {
            this.Text = "Tetris";
            this.ClientSize = new Size(200, 400); // Smaller pieces
            this.DoubleBuffered = true;

            LoadHighScore();

            game = new Game(UpdateHighScore);

            gameTimer = new Timer();
            gameTimer.Interval = 200; // Faster game speed
            gameTimer.Tick += GameTimer_Tick;
            gameTimer.Start();

            this.KeyDown += TetrisForm_KeyDown;
        }

        private void LoadHighScore()
        {
            if (File.Exists(HighScoreFile))
            {
                int.TryParse(File.ReadAllText(HighScoreFile), out highScore);
            }
        }

        private void SaveHighScore()
        {
            File.WriteAllText(HighScoreFile, highScore.ToString());
        }

        private void UpdateHighScore(int score)
        {
            if (score > highScore)
            {
                highScore = score;
                SaveHighScore();
            }
        }

        private void GameTimer_Tick(object sender, EventArgs e)
        {
            if (!isPaused)
            {
                game.Update();
                RenderToBuffer();
                this.Invalidate();
            }
        }

        private void TetrisForm_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.P)
            {
                isPaused = !isPaused;
                return;
            }

            if (!isPaused)
            {
                switch (e.KeyCode)
                {
                    case Keys.Left:
                        game.HandleInput(Game.Input.Left);
                        break;
                    case Keys.Right:
                        game.HandleInput(Game.Input.Right);
                        break;
                    case Keys.Down:
                        game.HandleInput(Game.Input.Down);
                        break;
                    case Keys.Up:
                        game.HandleInput(Game.Input.Rotate);
                        break;
                }
            }
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            e.Graphics.DrawImage(offscreenBuffer, 0, 0);
        }

        private Bitmap offscreenBuffer;

        private void RenderToBuffer()
        {
            using (Graphics g = Graphics.FromImage(offscreenBuffer))
            {
                g.Clear(Color.Black);
                game.Render(g, highScore);
            }
        }
    }

    public class Game
    {
        public enum Input { Left, Right, Down, Rotate }

        private int score;
        private bool[,] grid;
        private Tetromino currentTetromino;
        private Action<int> updateHighScoreCallback;

        public Game(Action<int> updateHighScoreCallback)
        {
            this.updateHighScoreCallback = updateHighScoreCallback;
            score = 0;
            grid = new bool[20, 10]; // 20 rows, 10 columns
            SpawnTetromino();
        }

        public void Update()
        {
            if (!currentTetromino.MoveDown(grid))
            {
                PlaceTetromino();
                ClearLines();
                SpawnTetromino();
            }
        }

        public void HandleInput(Input input)
        {
            switch (input)
            {
                case Input.Left:
                    currentTetromino.MoveLeft(grid);
                    break;
                case Input.Right:
                    currentTetromino.MoveRight(grid);
                    break;
                case Input.Down:
                    currentTetromino.MoveDown(grid);
                    break;
                case Input.Rotate:
                    currentTetromino.Rotate(grid);
                    break;
            }
        }

        public void Render(Graphics g, int highScore)
        {
            // Draw grid
            for (int row = 0; row < grid.GetLength(0); row++)
            {
                for (int col = 0; col < grid.GetLength(1); col++)
                {
                    if (grid[row, col])
                    {
                        g.FillRectangle(Brushes.Blue, col * 20, row * 20, 18, 18); // Smaller blocks
                    }
                }
            }

            // Draw current tetromino
            foreach (var block in currentTetromino.Blocks)
            {
                g.FillRectangle(Brushes.Red, block.Col * 20, block.Row * 20, 18, 18); // Smaller blocks
            }

            // Draw score and high score
            g.DrawString("Score: " + score, new Font("Arial", 12), Brushes.White, new PointF(10, 10));
            g.DrawString("High Score: " + highScore, new Font("Arial", 12), Brushes.White, new PointF(10, 30));
        }

        private void SpawnTetromino()
        {
            currentTetromino = TetrominoFactory.CreateRandomTetromino();
        }

        private void PlaceTetromino()
        {
            foreach (var block in currentTetromino.Blocks)
            {
                grid[block.Row, block.Col] = true;
            }
        }

        private void ClearLines()
        {
            for (int row = 0; row < grid.GetLength(0); row++)
            {
                bool fullLine = true;
                for (int col = 0; col < grid.GetLength(1); col++)
                {
                    if (!grid[row, col])
                    {
                        fullLine = false;
                        break;
                    }
                }
                if (fullLine)
                {
                    ClearLine(row);
                    score += 100;
                    updateHighScoreCallback(score);
                }
            }
        }

        private void ClearLine(int row)
        {
            for (int col = 0; col < grid.GetLength(1); col++)
            {
                grid[row, col] = false;
            }
            for (int r = row; r > 0; r--)
            {
                for (int col = 0; col < grid.GetLength(1); col++)
                {
                    grid[r, col] = grid[r - 1, col];
                }
            }
        }
    }

    public static class TetrominoFactory
    {
        private static readonly Random random = new Random();

        public static Tetromino CreateRandomTetromino()
        {
            int type = random.Next(0, 7); // 7 types of Tetris pieces
            switch (type)
            {
                case 0: return new Tetromino(new[] { new Block(0, 4), new Block(1, 4), new Block(2, 4), new Block(2, 5) }); // L-shape
                case 1: return new Tetromino(new[] { new Block(0, 4), new Block(0, 5), new Block(1, 4), new Block(1, 5) }); // Square
                case 2: return new Tetromino(new[] { new Block(0, 4), new Block(1, 4), new Block(2, 4), new Block(3, 4) }); // Line
                case 3: return new Tetromino(new[] { new Block(0, 4), new Block(1, 4), new Block(1, 5), new Block(2, 5) }); // Z-shape
                case 4: return new Tetromino(new[] { new Block(0, 5), new Block(1, 5), new Block(1, 4), new Block(2, 4) }); // S-shape
                case 5: return new Tetromino(new[] { new Block(0, 4), new Block(1, 4), new Block(1, 5), new Block(2, 4) }); // T-shape
                case 6: return new Tetromino(new[] { new Block(0, 4), new Block(1, 4), new Block(2, 4), new Block(2, 3) }); // Reverse L-shape
                default: throw new Exception("Invalid Tetromino type");
            }
        }
    }

    public class Tetromino
    {
        public List<Block> Blocks { get; private set; }

        public Tetromino(IEnumerable<Block> blocks)
        {
            Blocks = new List<Block>(blocks);
        }

        public bool MoveDown(bool[,] grid)
        {
            if (CanMove(1, 0, grid))
            {
                for (int i = 0; i < Blocks.Count; i++)
                {
                    Blocks[i] = new Block(Blocks[i].Row + 1, Blocks[i].Col);
                }
                return true;
            }
            return false;
        }

        public void MoveLeft(bool[,] grid)
        {
            if (CanMove(0, -1, grid))
            {
                for (int i = 0; i < Blocks.Count; i++)
                {
                    Blocks[i] = new Block(Blocks[i].Row, Blocks[i].Col - 1);
                }
            }
        }

        public void MoveRight(bool[,] grid)
        {
            if (CanMove(0, 1, grid))
            {
                for (int i = 0; i < Blocks.Count; i++)
                {
                    Blocks[i] = new Block(Blocks[i].Row, Blocks[i].Col + 1);
                }
            }
        }

        public void Rotate(bool[,] grid)
        {
            var pivot = Blocks[1]; // Use the second block as the pivot
            var newPositions = new List<Block>();

            foreach (var block in Blocks)
            {
                int newRow = pivot.Row - (block.Col - pivot.Col);
                int newCol = pivot.Col + (block.Row - pivot.Row);
                if (newRow < 0 || newRow >= grid.GetLength(0) || newCol < 0 || newCol >= grid.GetLength(1) || grid[newRow, newCol])
                {
                    return; // Invalid rotation
                }
                newPositions.Add(new Block(newRow, newCol));
            }

            Blocks = newPositions;
        }

        private bool CanMove(int rowDelta, int colDelta, bool[,] grid)
        {
            foreach (var block in Blocks)
            {
                int newRow = block.Row + rowDelta;
                int newCol = block.Col + colDelta;
                if (newRow < 0 || newRow >= grid.GetLength(0) || newCol < 0 || newCol >= grid.GetLength(1) || grid[newRow, newCol])
                {
                    return false;
                }
            }
            return true;
        }
    }

    public class Block
    {
        public int Row { get; private set; }
        public int Col { get; private set; }

        public Block(int row, int col)
        {
            Row = row;
            Col = col;
        }
    }
}