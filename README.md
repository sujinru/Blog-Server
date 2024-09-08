# Blog System Frontend Instructions

Access the Blog System at: http://54.167.33.160:5000/

## 1. Create Blog Entry

1. On the main page, locate the "Create a New Blog Post" section.
2. Fill in the following fields:
   - Title: Enter the title of your blog post
   - Content: Enter the content of your blog post
   - Author ID: Enter a numeric ID for the author (if you don't have an ID, enter any positive integer)
3. Click the "Create Blog" button.
4. You should see a success message, and the new blog post should appear in the list below.

Note: The system validates that the Author ID is a non-negative integer. If you enter an invalid ID, you'll see an error message.

## 2. Read Blog Entry

Individual blog entries are displayed in the "Blog Posts" section on the main page. Each entry shows:
- Title
- Content (first 100 characters)
- Author ID
- Creation Date

To view a full blog post:
1. Look for the blog post you want to read in the list.
2. The full content should be visible if it's less than 100 characters. If it's longer, you'll see "..." at the end.

Note: The current frontend doesn't provide a way to view the full content of long posts. This could be improved in future versions.

## 3. Read All Blog Entries

All blog entries are automatically displayed in the "Blog Posts" section when you load or refresh the page at http://54.167.33.160:5000/

Note: The current implementation doesn't include pagination or filtering. All posts are loaded at once, which could be slow if there are many posts.

## 4. Update Blog Entry

1. In the "Blog Posts" section, find the blog post you want to update.
2. Click the "Update" button next to the blog post.
3. The update form will appear, pre-filled with the current title and content.
4. Modify the title and/or content as desired.
5. Click the "Update Blog" button to save your changes.
6. The blog list should refresh, showing your updated post.

## 5. Delete Blog Entry

1. In the "Blog Posts" section, find the blog post you want to delete.
2. Click the "Delete" button next to the blog post.
3. The blog post should disappear from the list immediately.

