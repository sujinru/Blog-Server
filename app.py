from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime

from component import db, Platform, User, Blog, UserPlatform
from logger import logger

def create_app():
    app = Flask(__name__, static_folder='static')
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sjr5269898@localhost/blog_system'
    db.init_app(app)

    @app.route('/blog', methods=['POST'])
    def create_blog():
        logger.info('Attempting to create a new blog post')
        data = request.json

        # Validate authorid
        try:
            authorid = int(data['authorid'])
            if authorid < 0:
                raise ValueError("Author ID must be a non-negative integer")
        except (ValueError, KeyError):
            logger.warning(f'Invalid authorid: {data.get("authorid")}')
            return jsonify({'error': 'Invalid author ID. Must be a non-negative integer.'}), 400

        # Check if the author exists, if not, create a new user
        author = User.query.get(authorid)
        if not author:
            logger.info(f'Author not found for id: {authorid}. Creating new user.')
            new_user = User(
                userid=authorid,
                username=f'user_{authorid}',  # Generate a default username
                password='default_password',  # You might want to generate a random password
                role='user'
            )
            db.session.add(new_user)
            db.session.flush()  # This assigns the ID to the new_user object
            author = new_user

        new_blog = Blog(
            title=data['title'],
            content=data['content'],
            authorid=author.userid,
            datecreated=datetime.utcnow(),
            datemodified=datetime.utcnow(),
            isdeleted=False
        )

        db.session.add(new_blog)
        db.session.commit()

        logger.info(f'Blog created successfully: {new_blog.blogid}')
        return jsonify({
            'message': 'Blog created successfully',
            'blogid': new_blog.blogid,
            'title': new_blog.title,
            'authorid': new_blog.authorid
        }), 201

    # Read API (all blogs)
    @app.route('/blog', methods=['GET'])
    def get_all_blogs():
        blogs = Blog.query.filter_by(isdeleted=False).all()
        return jsonify([{
            'blogid': blog.blogid,
            'title': blog.title,
            'content': blog.content,
            'authorid': blog.authorid,
            'datecreated': blog.datecreated.isoformat(),
            'datemodified': blog.datemodified.isoformat()
        } for blog in blogs])

    # Read API (single blog)
    @app.route('/blog/<int:blogid>', methods=['GET'])
    def get_blog(blogid):
        blog = Blog.query.filter_by(blogid=blogid, isdeleted=False).first_or_404()
        return jsonify({
            'blogid': blog.blogid,
            'title': blog.title,
            'content': blog.content,
            'authorid': blog.authorid,
            'datecreated': blog.datecreated.isoformat(),
            'datemodified': blog.datemodified.isoformat()
        })

    # Update API
    @app.route('/blog/<int:blogid>', methods=['PUT'])
    def update_blog(blogid):
        blog = Blog.query.filter_by(blogid=blogid, isdeleted=False).first_or_404()
        data = request.json
        blog.title = data.get('title', blog.title)
        blog.content = data.get('content', blog.content)
        blog.datemodified = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Blog updated successfully'})

    # Delete API (soft delete)
    @app.route('/blog/<int:blogid>', methods=['DELETE'])
    def delete_blog(blogid):
        blog = Blog.query.filter_by(blogid=blogid, isdeleted=False).first_or_404()
        blog.isdeleted = True
        blog.datemodified = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Blog deleted successfully'})

    @app.route('/')
    def serve_ui():
        try:
            logger.info('Serving UI')
            return send_from_directory(app.static_folder, 'index.html')
        except Exception as e:
            logger.error(f"Error serving UI: {str(e)}")
            return f"Error serving UI: {str(e)}", 500

    # Add this new route for debugging
    @app.route('/debug')
    def debug_info():
        logger.debug('Accessing debug info')
        static_folder = app.static_folder
        index_path = os.path.join(static_folder, 'index.html')
        return {
            'static_folder': static_folder,
            'index_exists': os.path.exists(index_path),
            'current_directory': os.getcwd(),
            'directory_contents': os.listdir(os.getcwd()),
            'static_contents': os.listdir(static_folder) if os.path.exists(static_folder) else 'Static folder does not exist'
        }

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    return app

if __name__ == '__main__':
    app = create_app()
    logger.info('Starting the Flask application')
    app.run(host='0.0.0.0', port=5000, debug=True)