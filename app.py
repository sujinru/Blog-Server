from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='static')
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sjr5269898@localhost/blog_system'
    db.init_app(app)

    class Platform(db.Model):
        __tablename__ = 'platform'
        __table_args__ = {'schema': 'public'}

        platformid = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), nullable=False)
        description = db.Column(db.Text)
        datecreated = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    class UserPlatform(db.Model):
        __tablename__ = 'userplatform'
        __table_args__ = {'schema': 'public'}

        userplatformid = db.Column(db.Integer, primary_key=True)
        userid = db.Column(db.Integer, db.ForeignKey('public.User.userid'), nullable=False)
        platformid = db.Column(db.Integer, db.ForeignKey('public.platform.platformid'), nullable=False)
        datejoined = db.Column(db.Date, nullable=False, default=datetime.utcnow)

        user = db.relationship('User', backref=db.backref('userplatforms', lazy=True))
        platform = db.relationship('Platform', backref=db.backref('userplatforms', lazy=True))

    class User(db.Model):
        __tablename__ = 'User'
        __table_args__ = {'schema': 'public'}

        userid = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(255), unique=True, nullable=False)
        password = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(255))
        firstname = db.Column(db.String(255))
        lastname = db.Column(db.String(255))
        role = db.Column(db.String(50), nullable=False)
        datecreated = db.Column(db.Date, nullable=False, default=datetime.utcnow)
        datemodified = db.Column(db.Date, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Blog(db.Model):
        __tablename__ = 'blog'
        __table_args__ = {'schema': 'public'}

        blogid = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(255), nullable=False)
        content = db.Column(db.Text, nullable=False)
        authorid = db.Column(db.Integer, db.ForeignKey('public.User.userid'), nullable=False)
        datecreated = db.Column(db.Date, nullable=False, default=datetime.utcnow)
        datemodified = db.Column(db.Date, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
        isdeleted = db.Column(db.Boolean, nullable=False, default=False)

        author = db.relationship('User', backref=db.backref('blogs', lazy=True))

    class Comment(db.Model):
        __tablename__ = 'comment'
        __table_args__ = {'schema': 'public'}

        commentid = db.Column(db.Integer, primary_key=True)
        content = db.Column(db.Text, nullable=False)
        authorid = db.Column(db.Integer, db.ForeignKey('public.User.userid'), nullable=False)
        blogid = db.Column(db.Integer, db.ForeignKey('public.blog.blogid'), nullable=False)
        datecreated = db.Column(db.Date, nullable=False, default=datetime.utcnow)
        datemodified = db.Column(db.Date, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
        isdeleted = db.Column(db.Boolean, nullable=False, default=False)

        author = db.relationship('User', backref=db.backref('comments', lazy=True))
        blog = db.relationship('Blog', backref=db.backref('comments', lazy=True))

    @app.route('/blog', methods=['POST'])
    def create_blog():
        data = request.json

        # Check if the author exists
        author = User.query.get(data['authorid'])
        if not author:
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
    def (blogid):
        blog = Blog.query.filter_by(blogid=blogid, isdeleted=False).first_or_404()
        blog.isdeleted = True
        blog.datemodified =delete_blog datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Blog deleted successfully'})

    @app.route('/')
    def serve_ui():
        try:
            return send_from_directory(app.static_folder, 'index.html')
        except Exception as e:
            app.logger.error(f"Error serving UI: {str(e)}")
            return f"Error serving UI: {str(e)}", 500

    # Add this new route for debugging
    @app.route('/debug')
    def debug_info():
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
    app.run(host='0.0.0.0', port=5000, debug=True)