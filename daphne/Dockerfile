FROM ninjaclasher/dmoj-base:latest
# Expose port for Daphne
EXPOSE 8000

# Start the application with Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]