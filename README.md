# Subscription App

## Project Structure
```
subscription_app/
├── config/           # Django project settings and configuration
│   ├── settings.py   # Main settings file
│   ├── urls.py       # Root URL configuration
│   └── ...
├── core/             # Main app for subscriptions, plans, features
│   ├── models.py     # Data models (Feature, Plan, Subscription)
│   ├── serializers.py# DRF serializers
│   ├── views.py      # API views and viewsets
│   ├── urls.py       # App-specific URL routing
│   └── tests/        # Unit and API tests
│       ├── test_subscription.py
│       └── test_subscription_api.py
├── identity/         # App for authentication/logout
│   └── ...
├── .gitignore        # Git ignore file
├── README.md         # Project documentation
├── pyproject.toml    # Poetry configuration
└── ...
```

## Optimizations Used
- **prefetch_related & select_related:**
  - Used in queryset methods to optimize DB queries and avoid N+1 problems when fetching related objects (e.g., plans and features for subscriptions).
- **Global Pagination:**
  - Enabled via DRF settings for all list endpoints to improve performance and API usability.
- **JWT Authentication:**
  - Secures all API endpoints using `rest_framework_simplejwt`. Only authenticated users can access protected resources.
- **Permission Classes:**
  - Admin-only access for plan/feature management; user-specific access for subscriptions.

## Security
- JWT authentication for all sensitive endpoints.
- Permissions restrict access to resources based on user roles.
- Environment files and secrets are excluded from version control via `.gitignore`.

## Testing
- Unit and API tests for subscriptions, plan switching, and nested data retrieval.
- Uses Django's test framework and DRF's `APITestCase`.

## Further Enhancements
- **Docker Setup:**
  - Add `Dockerfile` and `docker-compose.yml` for containerized development and deployment.
- **CI/CD Integration:**
  - Set up GitHub Actions or similar for automated testing and deployment.
- **API Rate Limiting:**
  - Add throttling for extra security and stability.
- **Swagger/OpenAPI Docs:**
  - Already integrated via drf-spectacular for interactive API docs.
- **Factory Boy for Test Data:**
  - Use Factory Boy for more maintainable and flexible test data creation.
- **Custom User Model:**
  - Consider switching to a custom user model for extensibility.

## Quick Start
1. Install dependencies:
   ```sh
   poetry install
   ```
2. Run migrations:
   ```sh
   poetry run python manage.py migrate
   ```
3. Start the server:
   ```sh
   poetry run python manage.py runserver
   ```
4. Run tests:
   ```sh
   poetry run python manage.py test core.tests
   ```

## API Authentication
- Obtain JWT token via `/api/auth/token/`.
- Use the token in the `Authorization: Bearer <token>` header for all requests.

## Contact
For questions or suggestions, open an issue or contact the maintainer.
