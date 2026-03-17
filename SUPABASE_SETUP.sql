-- ==============================================================================
-- Supabase User Table Setup for OptimizeHub
-- ==============================================================================
-- Run this SQL in your Supabase Dashboard → SQL Editor → New Query
-- ==============================================================================

-- Create profiles table (extends auth.users)
-- This table stores additional user information like username
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Users can view their own profile
CREATE POLICY "Users can view own profile" 
ON public.profiles
FOR SELECT
USING (auth.uid() = id);

-- Policy: Users can update their own profile
CREATE POLICY "Users can update own profile" 
ON public.profiles
FOR UPDATE
USING (auth.uid() = id);

-- Policy: Users can insert their own profile (for signup)
CREATE POLICY "Users can insert own profile" 
ON public.profiles
FOR INSERT
WITH CHECK (auth.uid() = id);

-- Optional: Create an index on username for faster lookups
CREATE INDEX IF NOT EXISTS profiles_username_idx ON public.profiles(username);

-- Optional: Create an index on email for faster lookups
CREATE INDEX IF NOT EXISTS profiles_email_idx ON public.profiles(email);

-- ==============================================================================
-- Notes:
-- ==============================================================================
-- 1. The profiles table extends Supabase's built-in auth.users table
-- 2. The id column references auth.users(id) and will be automatically set
--    when a user signs up through Supabase Auth
-- 3. RLS policies ensure users can only access their own data
-- 4. The updated_at column automatically tracks when profiles are modified
-- ==============================================================================
