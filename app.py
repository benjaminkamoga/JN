from flask import Flask, render_template, request, flash, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages


# ---- Routes ----
@app.route('/')
def home():
    home_folder = os.path.join(app.static_folder, "images/home")
    home_images = [
        "images/home/" + f for f in os.listdir(home_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
    ]
    return render_template('index.html', images=home_images)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/products')
def products():
    """
    Dynamic product loader:
    Folder structure:
    static/images/products/<Category>/<Product>/<images + details.txt + price.txt>
    """
    product_root = os.path.join(app.static_folder, 'images', 'products')
    categories = {}

    if os.path.exists(product_root):
        for category_name in os.listdir(product_root):
            category_path = os.path.join(product_root, category_name)
            if os.path.isdir(category_path):
                products_list = []
                for product_folder in os.listdir(category_path):
                    product_path = os.path.join(category_path, product_folder)
                    if os.path.isdir(product_path):
                        # Collect images
                        images = [
                            f'images/products/{category_name}/{product_folder}/{f}'
                            for f in os.listdir(product_path)
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
                        ]

                        # Read description
                        description = ""
                        details_file = os.path.join(product_path, 'details.txt')
                        if os.path.exists(details_file):
                            with open(details_file, 'r', encoding='utf-8') as file:
                                description = file.read().strip()

                        # Read price
                        price = 0
                        price_file = os.path.join(product_path, 'price.txt')
                        if os.path.exists(price_file):
                            with open(price_file, 'r', encoding='utf-8') as file:
                                try:
                                    price = int(file.read().strip())
                                except:
                                    price = 0

                        products_list.append({
                            'name': product_folder.replace('_', ' ').title(),
                            'images': images,
                            'description': description,
                            'price': price
                        })

                categories[category_name] = products_list

    return render_template('products.html', categories=categories)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_body = request.form.get('message')

        if not email or not message_body:
            flash("Email and Message are required!", "danger")
            return redirect(url_for('contact'))

        # For now, just confirm receipt — no email sending
        flash("Your message has been received! (Email sending disabled for now)", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
