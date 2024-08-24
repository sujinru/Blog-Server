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

        # Check if the author exists
        author = User.query.get(data['authorid'])
        if not author:
            logger.warning(f'Author not found for id: {data["authorid"]}')
            return jsonify({'error': 'Author not found'}), 404

        new_blog = Blog(
            title=data['title'],
            content=data['content'],
            authorid=data['authorid'],
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