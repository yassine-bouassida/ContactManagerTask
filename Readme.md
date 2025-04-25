# Setup Contact Manager

This is a Django + HTMX + Tailwind CDN + PostgreSQL project, managed via Docker Compose. Follow these steps to launch each service in its own terminal and see live logs and test output.

## Prerequisites

- Docker and Docker Compose installed
- A `.env` file at the project root containing:
  ```env
  DEBUG=1
  SECRET_KEY=your-secret-key
  PG_DB=contacts_db
  PG_USER=postgres
  PG_PASS=postgres
  ```

## Launching Services

Open three separate terminal windows or tabs, cd into the project root in each.

### Terminal 1: Database

Start the PostgreSQL container and view its logs:

```bash
docker-compose up db
```

### Terminal 2: Tests

Run migrations and the test suite. The container will exit when done:

```bash
docker-compose run --rm test
```

Re-run this command anytime you want to see updated test results.

### Terminal 3: Web Server

Start the Django development server (auto-runs migrations on startup):

```bash
docker-compose up web
```

The application will be available at [http://localhost:8000](http://localhost:8000).

## Cleanup

To stop all running containers and remove networks:

```bash
docker-compose down
```

## Why this stack?

I’ve been testing this combination lately and it’s hands‑down one of the fastest for spinning up a demo:

- **Django**: Rapid project scaffolding and built‑in admin, ORM, and migration system.
- **HTMX**: Tiny JS library to add AJAX interactions without a frontend framework.
- **Tailwind (CDN)**: Zero‑build CSS utility library—add styles via CDN for instant feedback.
- **PostgreSQL**: Reliable open‑source database with minimal setup.
- **Docker Compose**: Keeps everything containerized, so you can launch the full stack with a single command.

# Trade‑Offs & Known Issues

This document outlines design trade‑offs made and small bugs to be aware of in the Contact Manager project.

---

## 1. Backend vs. Frontend Search

**Trade‑Off**: We perform search filtering on the server side (via Django ORM) rather than in the browser.

- **Pros**

  - Handles large datasets without shipping all data to the client.
  - Can leverages database indexing for fast lookups.

- **Cons**

  - Increased latency on each keystroke, since each filter event issues an HTTP request.
  - Higher network overhead compared to client‑side filtering.
  - UX feels slightly less snappy for extremely rapid typing.

---

## 2. Tailwind via CDN

**Trade‑Off**: Using Tailwind through its CDN version rather than a local build step.

- **Pros**

  - Zero build pipeline, instant setup and feedback.
  - Always up to date with the latest utility classes.

- **Cons**

  - Larger initial CSS payload (no tree‑shaking or PurgeCSS).
  - Potential for unused classes to bloat page download size.

**Possible Improvement**: Migrate to a local Tailwind build with PurgeCSS to strip out unused styles in production.

---

## 3. Known Bug: Adding While Filtered

**Symptom**: If you have a search term applied (e.g. searching for “Alice”) and then add a new contact whose name does **not** match the current filter, the new card still appears in the list.

- **Cause**: The HTMX `hx-swap="beforeend"` blindly appends the new card to `#list` without re-checking the current filter term.

- **Workaround**: Clear the search input before adding, or perform a full reload of the list after adding.

- **Possible Fix**: After a successful add, re-issue the same search query via HTMX to reload the filtered list. For example:

  ```html
  <button
    hx-include="[name=search]"
    hx-post="..."
    hx-target="#list"
    hx-swap="innerHTML"
  >Add</button>
  ```

---

## 4. Test Coverage Limitations

**Observation**: Tests are minimal due to time constraints and primarily cover basic create/delete flows via HTMX.

- Missing edge‑case tests around validation errors, form behaviors, and search filtering.
- No tests for UI states (e.g. error message clearing, delete confirmation prompts).

**Possible Improvement**: Expand tests to include:

- Validation error scenarios (duplicate email, invalid input).
- Search functionality when typing and clearing filters.
- Delete confirmation flow.

---

## Final Note

This project was coded entirely within the timeframe. Architectural planning began beforehand, documentation and GitHub setup happened afterward, and Tailwind CSS  was generated using AI.










