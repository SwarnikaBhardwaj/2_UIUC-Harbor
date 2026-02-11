from django.db import models
from django.core.validators import EmailValidator

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    university_email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text="Must be a valid .edu email address"
    )
    phone_number = models.CharField(max_length=15, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['university_email'],
                name='unique_student_email'
            )
        ]
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.university_email})"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.university_email})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('student_detail', args=[str(self.id)])

class Category(models.Model):
    CATEGORY_TYPES = [
        ('SERVICE', 'Service'),
        ('FUNDRAISER', 'Fundraiser'),
        ('SELLER', 'Seller'),
    ]
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    description = models.TextField(max_length=300, blank=True)
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category_type'],
                name='unique_category_name_per_type'
            )
        ]
    def __str__(self):
        return f"{self.name} ({self.category_type})"

    def __str__(self):
        return f"{self.name} ({self.category_type})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('category_detail', args=[str(self.id)])

class Listing(models.Model):
    PAYMENT_METHODS = [
        ('VENMO', 'Venmo'),
        ('CASH', 'Cash'),
        ('PAYPAL', 'PayPal'),
        ('ZELLE', 'Zelle'),
    ]
    seller = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='listings'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price in USD (leave blank for free/donations)"
    )
    contact_method = models.CharField(max_length=200)
    accepted_payment = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='VENMO'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['seller', 'title'],
                name='unique_listing_per_seller'
            )
        ]
    def __str__(self):
        return f"{self.title} by {self.seller.first_name}"

    def __str__(self):
        return f"{self.title} by {self.seller.first_name}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('listing_detail', args=[str(self.id)])

class Conversation(models.Model):
   student1 = models.ForeignKey(
       Student,
       on_delete=models.CASCADE,
       related_name='conversations_started'
   )
   student2 = models.ForeignKey(
       Student,
       on_delete=models.CASCADE,
       related_name='conversations_received'
   )
   listing = models.ForeignKey(
       Listing,
       on_delete=models.SET_NULL,
       null=True,
       blank=True
   )
   last_message_at = models.DateTimeField(null=True, blank=True)
   created_at = models.DateTimeField(auto_now_add=True)


   def __str__(self):
       return f"Conversation between {self.student1} and {self.student2}"


class Message(models.Model):
   conversation = models.ForeignKey(
       Conversation,
       on_delete=models.CASCADE,
       related_name='messages'
   )
   sender = models.ForeignKey(
       Student,
       on_delete=models.CASCADE,
       related_name='sent_messages'
   )
   receiver = models.ForeignKey(
       Student,
       on_delete=models.CASCADE,
       related_name='received_messages'
   )
   message_text = models.TextField()
   is_read = models.BooleanField(default=False)
   created_at = models.DateTimeField(auto_now_add=True)


   def __str__(self):
       return f"Message from {self.sender}"


class ServiceRequest(models.Model):
   requester = models.ForeignKey(
       Student,
       on_delete=models.CASCADE,
       related_name='service_requests'
   )
   category = models.ForeignKey(
       Category,
       on_delete=models.PROTECT
   )
   title = models.CharField(max_length=200)
   description = models.TextField()
   budget = models.DecimalField(
       max_digits=10,
       decimal_places=2,
       null=True,
       blank=True
   )
   preferred_contact = models.CharField(max_length=200)
   is_fulfilled = models.BooleanField(default=False)
   created_at = models.DateTimeField(auto_now_add=True)


   def __str__(self):
       return self.title


class Review(models.Model):
   reviewer = models.ForeignKey(
       Student,
       on_delete=models.CASCADE,
       related_name='reviews_given'
   )
   reviewed_student = models.ForeignKey(
       Student,
       on_delete=models.CASCADE,
       related_name='reviews_received'
   )
   listing = models.ForeignKey(
       Listing,
       on_delete=models.CASCADE
   )
   rating = models.PositiveSmallIntegerField()
   review_text = models.TextField(blank=True)
   created_at = models.DateTimeField(auto_now_add=True)


   def __str__(self):
       return f"Review by {self.reviewer}"
