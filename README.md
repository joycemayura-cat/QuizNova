<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>QuizNova | Interactive Learning</title>

    <link rel="stylesheet"
          href="{{ url_for('static', filename='style.css') }}">
</head>

<body>

<nav class="navbar">

    <div class="logo">
        <span>⚡</span> QuizNova
    </div>

    <div class="nav-links">
        <a href="/">Home</a>
        <a href="/create">Create Quiz</a>
        <a href="/join">Join Quiz</a>
    </div>

</nav>


<section class="hero">

    <div class="hero-content">

        <div class="badge">
            🚀 Interactive Learning Platform
        </div>

        <h1>
            Make Learning
            <span>Fun & Interactive</span>
        </h1>

        <p>
            Create engaging quizzes, challenge your students,
            and see results instantly.
        </p>

        <div class="hero-buttons">

            <a href="/create" class="btn primary">
                Create a Quiz →
            </a>

            <a href="/join" class="btn secondary">
                Join Quiz
            </a>

        </div>

    </div>


    <div class="quiz-preview">

        <div class="preview-header">
            <span>Python Fundamentals</span>
            <span class="timer">⏱ 00:42</span>
        </div>

        <div class="progress">
            <div></div>
        </div>

        <p class="question-number">
            Question 3 of 10
        </p>

        <h2>
            Which language is used to style web pages?
        </h2>

        <div class="preview-options">

            <div>A. Python</div>
            <div class="correct">B. CSS ✓</div>
            <div>C. Java</div>
            <div>D. C++</div>

        </div>

    </div>

</section>


<section class="features">

    <h2>Everything You Need</h2>

    <p class="section-subtitle">
        A simple platform for interactive education.
    </p>

    <div class="feature-grid">

        <div class="feature-card">
            <div class="icon">📝</div>
            <h3>Create Quizzes</h3>
            <p>
                Build quizzes with multiple-choice questions.
            </p>
        </div>

        <div class="feature-card">
            <div class="icon">🔑</div>
            <h3>Join with Code</h3>
            <p>
                Students can join using a unique quiz code.
            </p>
        </div>

        <div class="feature-card">
            <div class="icon">🏆</div>
            <h3>Live Results</h3>
            <p>
                Automatically calculate scores and rankings.
            </p>
        </div>

        <div class="feature-card">
            <div class="icon">📊</div>
            <h3>Leaderboard</h3>
            <p>
                Compare student performance instantly.
            </p>
        </div>

    </div>

</section>


<footer>
    © 2026 QuizNova — Interactive Learning Platform
</footer>

</body>
</html>
