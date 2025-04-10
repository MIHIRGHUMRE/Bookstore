from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # To protect views if needed
from .models import Book, Publication

def book_list(request):
    """Displays the list of all available books."""
    books = Book.objects.all().order_by('title')
    # Get cart item count for display in navbar (optional)
    cart = request.session.get('cart', {})
    cart_item_count = sum(cart.values())
    context = {
        'books': books,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'bookstore_app/book_list.html', context)

def add_to_cart(request, book_id):
    """Adds a book to the session-based cart."""
    book = get_object_or_404(Book, id=book_id)
    # Get the cart dictionary from session, or create an empty one
    cart = request.session.get('cart', {})

    # Get current quantity for the book, default to 0 if not in cart
    quantity = cart.get(str(book_id), 0)
    # Increment quantity
    cart[str(book_id)] = quantity + 1

    # Save the updated cart back into the session
    request.session['cart'] = cart
    # Mark session as modified to ensure it's saved
    request.session.modified = True

    # Redirect back to the book list page (or wherever you prefer)
    return redirect('book_list')

def view_cart(request):
    """Displays the items currently in the cart."""
    cart_dict = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    # Retrieve book objects and calculate totals
    for book_id, quantity in cart_dict.items():
        try:
            book = Book.objects.get(id=int(book_id))
            item_total = book.price * quantity
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'item_total': item_total,
            })
            total_price += item_total
        except Book.DoesNotExist:
            # If a book in the cart was deleted from DB, remove it from session cart
            del cart_dict[book_id]
            request.session['cart'] = cart_dict
            request.session.modified = True
            # Optionally add a message to the user
            # messages.warning(request, f"A book previously in your cart is no longer available and has been removed.")

    # Get cart item count for display in navbar (optional)
    cart_item_count = sum(cart_dict.values())

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_item_count': cart_item_count, # Pass count for consistency if navbar uses it
    }
    return render(request, 'bookstore_app/cart.html', context)

def remove_from_cart(request, book_id):
    """Removes an item completely from the cart."""
    cart = request.session.get('cart', {})
    book_id_str = str(book_id) # Use string key

    if book_id_str in cart:
        del cart[book_id_str]
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('view_cart') # Redirect back to the cart page

def checkout(request):
    """Simulates a checkout process, clears the cart."""
    if request.method == 'POST': # Only process POST requests (from the form)
        cart = request.session.get('cart', {})

        if cart: # Only clear cart if it's not already empty
            # Simulate payment processing here (in a real app, you'd integrate with a payment gateway)
            # For now, we just print a message to the console (optional)
            print("Simulating payment...")
            print("Payment successful!")

            # Clear the cart in the session
            request.session['cart'] = {}
            request.session.modified = True

            # You could add a success message to display on the cart page
            success_message = "Payment successful! Thank you for your order."
            cart_item_count = 0 # Cart is now empty

            context = {
                'cart_items': [], # Pass empty cart items to template
                'total_price': 0,
                'cart_item_count': cart_item_count,
                'success_message': success_message, # Pass the success message to the template
            }
            return render(request, 'bookstore_app/cart.html', context) # Re-render the cart page with success message

    # If it's not a POST request (e.g., someone types /cart/checkout/ in URL bar directly),
    # just redirect them back to the cart page.
    return redirect('view_cart')