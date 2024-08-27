document.addEventListener('DOMContentLoaded', function () {
    const stripe = Stripe('{{ public_key }}'); // Stripe public key from settings
    const elements = stripe.elements();
  
    // Create an instance of Elements
    const cardElement = elements.create('card');
    cardElement.mount('#card-element');
  
    const form = document.getElementById('payment-form');
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
  
      const {error, paymentIntent} = await stripe.confirmCardPayment('{{ client_secret }}', {
        payment_method: {
          card: cardElement,
        },
      });
  
      if (error) {
        document.getElementById('error-message').textContent = error.message;
      } else {
        if (paymentIntent.status === 'succeeded') {
          window.location.href = "{% url 'success' %}";
        }
      }
    });
  });
  