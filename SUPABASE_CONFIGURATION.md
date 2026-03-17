# Supabase Configuration Guide for OptimizeHub

## ✅ Required Configuration

### 1. Enable Email Provider (Default: Already Enabled)

The email provider is enabled by default in Supabase. No action needed unless you disabled it.

**To verify:**
1. Go to Supabase Dashboard → **Authentication** → **Providers**
2. Ensure **Email** is enabled (toggle should be ON)

### 2. Email Confirmation Settings (Optional)

By default, Supabase requires email confirmation. For development, you can disable this for faster testing.

**Option A: Disable Email Confirmation (Development)**
1. Go to **Authentication** → **Settings** → **Email Auth**
2. Toggle OFF **"Enable email confirmations"**
3. Users can sign up and login immediately without email verification

**Option B: Keep Email Confirmation (Production Recommended)**
- Leave email confirmations enabled
- Users will receive a confirmation email after signup
- They must click the link before they can login
- More secure for production

### 3. Site URL Configuration

**For Development:**
1. Go to **Authentication** → **URL Configuration**
2. Set **Site URL** to: `http://localhost:5173` (or your frontend URL)
3. Add to **Redirect URLs**: 
   - `http://localhost:5173`
   - `http://localhost:5173/**`
   - `http://127.0.0.1:5173`

**For Production:**
- Set **Site URL** to your production domain (e.g., `https://yourdomain.com`)
- Add production URLs to **Redirect URLs**

## ❌ NOT Required (OAuth is Optional)

### OAuth Providers (Google, GitHub, etc.)

**You do NOT need to enable OAuth** for basic email/password authentication. OAuth is only needed if you want users to sign in with:
- Google
- GitHub
- Facebook
- Apple
- etc.

**If you want to add OAuth later:**
1. Go to **Authentication** → **Providers**
2. Enable the provider you want (e.g., Google)
3. Add OAuth credentials (Client ID, Client Secret)
4. Update your frontend to include OAuth buttons

## 🔒 Security Settings

### Password Requirements

**Default settings are usually fine, but you can customize:**
1. Go to **Authentication** → **Settings** → **Password**
2. Configure:
   - Minimum password length (default: 6)
   - Password complexity requirements
   - Password history (prevent reuse)

### Rate Limiting

Supabase has built-in rate limiting to prevent abuse:
- Login attempts: Limited per IP
- Signup attempts: Limited per IP
- Password reset: Limited per email

**To view/adjust:**
- Go to **Authentication** → **Settings** → **Rate Limits**

## 📧 Email Templates (Optional)

You can customize email templates for:
- Email confirmation
- Password reset
- Magic link (if enabled)

**To customize:**
1. Go to **Authentication** → **Email Templates**
2. Edit the templates as needed
3. Use variables like `{{ .ConfirmationURL }}` for dynamic content

## ✅ Quick Setup Checklist

- [ ] Email provider is enabled
- [ ] Site URL is set to `http://localhost:5173` (for dev)
- [ ] Redirect URLs include your frontend URL
- [ ] Email confirmation is configured (enabled for prod, optional for dev)
- [ ] Database schema is created (run `SUPABASE_SETUP.sql`)
- [ ] Environment variables are set in backend `.env`
- [ ] Environment variables are set in frontend `.env`

## 🧪 Testing Your Setup

### Test Signup Flow:
1. Try signing up with a new email
2. Check if user is created in **Authentication** → **Users**
3. Check if profile is created in **Table Editor** → **profiles**
4. Try logging in with the credentials

### Test Login Errors:
1. Try logging in with non-existent email → Should show "No account found"
2. Try logging in with wrong password → Should show "Invalid email or password"
3. Try logging in with unconfirmed email (if confirmation enabled) → Should show verification message

## 🐛 Common Issues

### Issue: "User already registered" but can't login
**Solution:** Check if email confirmation is required. User might need to verify email first.

### Issue: "Invalid credentials" for correct password
**Solution:** 
- Check if email confirmation is enabled and user hasn't confirmed
- Verify password hasn't been changed
- Check Supabase logs in Dashboard → **Logs** → **Auth Logs**

### Issue: CORS errors
**Solution:** 
- Verify Site URL and Redirect URLs are set correctly
- Check backend CORS configuration includes your frontend URL

### Issue: Profile not created after signup
**Solution:**
- Check Supabase logs for errors
- Verify RLS policies allow inserts
- Check that service_role key is set correctly in backend `.env`

## 📚 Additional Resources

- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [Supabase Email Templates](https://supabase.com/docs/guides/auth/auth-email-templates)
- [Supabase RLS Guide](https://supabase.com/docs/guides/auth/row-level-security)
