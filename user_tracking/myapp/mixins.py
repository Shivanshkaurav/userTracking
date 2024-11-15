from django.db import models

class TrackableMixin(models.Model):
    class Meta:
        abstract = True
    
    def track_changes(self, action, details=None):
        from .models import TodoTracking
        
        # Dynamically generate details if not provided
        if not details:
            details = self._generate_details(action)
        
        # Ensure user or customer is captured
        user = getattr(self, 'user', None) or getattr(self, 'customer', None)
        
        if user:  # If 'user' or 'customer' exists, use it
            TodoTracking.objects.create(
                user=user,  # This will work for both 'user' and 'customer'
                action=action,
                model_name=self.__class__.__name__,
                model_instance_id=self.id,
                details=details
            )
    
    def _generate_details(self, action):
        """
        Generates a generic detail description for any model.
        Can be customized further based on your requirements.
        """
        model_name = self.__class__.__name__
        field_names = [field.name for field in self._meta.fields]
        
        if action == 'Created':
            # Generate a list of field names and values for creation
            field_values = ", ".join([f"{field}: {getattr(self, field, 'N/A')}" for field in field_names])
            
            # Add timestamp if available
            timestamp = getattr(self, 'created_at', None) or getattr(self, 'timestamp', None)
            if timestamp:
                field_values += f", created_at: {timestamp}"
                
            return f"Created {model_name}: {field_values}"
        
        elif action == 'Deleted':
            # For deletion, list all field values of the object being deleted
            field_values = ", ".join([f"{field}: {getattr(self, field, 'N/A')}" for field in field_names])
            return f"Deleted {model_name}: {field_values}"
        
        else:
            # For updates, list the changed fields (optional)
            return f"{model_name} action: {action} on ID {self.id}"
