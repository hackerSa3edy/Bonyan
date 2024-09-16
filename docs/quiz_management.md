# Quiz Management System

## Description
Develop a comprehensive quiz management system for quiz creators to create, edit, and manage quizzes.

## Tasks
1. Implement quiz creation functionality
2. Develop question management system
3. Create quiz settings and configuration options
4. Design and implement quiz assignment system

## Technical Specifications

### Quiz Creation
- Design a quiz model with fields: id, title, description, creator_id, type (timed/untimed), start_time, end_time, created_at, updated_at
- Implement CRUD operations for quizzes
- Create an API for quiz management

### Question Management
- Design a question model with fields: id, quiz_id, question_text, question_type, options, correct_answer, points
- Implement CRUD operations for questions
- Create an API for question management within quizzes

### Quiz Settings and Configuration
- Implement settings for quiz visibility (public/private)
- Create options for result visibility and PDF download
- Develop a system for timed quizzes

### Quiz Assignment
- Design a quiz assignment model to link quizzes with users
- Implement functionality to assign quizzes to specific users by email

## API Endpoints
- POST /api/quizzes
- GET /api/quizzes
- GET /api/quizzes/:quiz_id
- PUT /api/quizzes/:quiz_id
- DELETE /api/quizzes/:quiz_id

- POST /api/quizzes/:quiz_id/publish
- POST /api/quizzes/:quiz_id/unpublish
- POST /api/quizzes/:quiz_id/assign

- POST /api/quizzes/:quiz_id/questions
- GET /api/quizzes/:quiz_id/questions
- GET /api/quizzes/:quiz_id/questions/:question_id
- PUT /api/quizzes/:quiz_id/questions/:question_id
- DELETE /api/quizzes/:quiz_id/questions/:question_id

## Database Schema

```sql
CREATE TABLE quizzes (
  id UUID PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  creator_id UUID REFERENCES users(id),
  start_time TIMESTAMP WITH TIME ZONE,
  end_time TIMESTAMP WITH TIME ZONE,
  is_public BOOLEAN DEFAULT FALSE,
  show_results BOOLEAN DEFAULT TRUE,
  allow_pdf_download BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE questions (
  id UUID PRIMARY KEY,
  quiz_id UUID REFERENCES quizzes(id),
  text TEXT NOT NULL,
  correct_answer UUID REFERENCES choices(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE choices (
  id UUID PRIMARY KEY,
  question_id UUID REFERENCES questions(id),
  text TEXT NOT NULL,
  is_correct BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quiz_assignments (
  id UUID PRIMARY KEY,
  quiz_id UUID REFERENCES quizzes(id),
  user_id UUID REFERENCES users(id),
  assigned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_answers (
    id UUID PRIMARY KEY,
    quiz_attempt_id UUID REFERENCES quiz_attempts(id),
    question_id UUID REFERENCES questions(id),
    user_answer JSONB,
    is_correct BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Mockup: Quiz Creation Page
### Creator Dashboard

![Creator Dashboard](assets/Creator%20Dashboard%20Page.png)
