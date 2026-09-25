"""
Movie Ticket Booking System
FastAPI backend with embedded HTML/CSS/JS frontend.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Movie Ticket Booking")

# ---------- In-memory data store ----------
movies = {
    1: {"name": "Avengers: Endgame", "price": 250, "seats": 50},
    2: {"name": "Inception",          "price": 200, "seats": 40},
    3: {"name": "Interstellar",       "price": 300, "seats": 30},
    4: {"name": "The Dark Knight",    "price": 220, "seats": 45},
    5: {"name": "Dune: Part Two",     "price": 280, "seats": 35},
    6: {"name": "Oppenheimer",        "price": 260, "seats": 25},
}
bookings = []


# ---------- Request model ----------
class BookingRequest(BaseModel):
    movie_id: int
    customer: str = Field(default="Guest", min_length=1)
    tickets: int = Field(gt=0)


# ---------- API routes ----------
@app.get("/api/movies")
def list_movies():
    return [
        {"id": mid, "name": m["name"], "price": m["price"], "seats": m["seats"]}
        for mid, m in movies.items()
    ]


@app.get("/api/bookings")
def list_bookings():
    return bookings


@app.post("/api/book", status_code=201)
def book_ticket(req: BookingRequest):
    movie = movies.get(req.movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    if req.tickets > movie["seats"]:
        raise HTTPException(
            status_code=400,
            detail=f"Only {movie['seats']} seats available",
        )

    movie["seats"] -= req.tickets
    total = req.tickets * movie["price"]
    booking = {
        "customer": req.customer,
        "movie": movie["name"],
        "tickets": req.tickets,
        "total": total,
    }
    bookings.append(booking)
    return {"status": "confirmed", **booking}


# ---------- Embedded UI ----------
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>🎬 Movie Ticket Booking</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #1e1e2f, #2b2b45);
    color: #fff;
    min-height: 100vh;
    padding: 30px 15px;
  }
  .container { max-width: 1100px; margin: 0 auto; }
  h1 {
    text-align: center;
    font-size: 2.2rem;
    margin-bottom: 10px;
    background: linear-gradient(90deg, #ffd166, #ef476f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .subtitle { text-align: center; color: #aaa; margin-bottom: 30px; }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 40px;
  }
  .movie-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 20px;
    transition: transform 0.2s, box-shadow 0.2s;
    backdrop-filter: blur(6px);
  }
  .movie-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
  }
  .movie-card h3 { font-size: 1.1rem; margin-bottom: 10px; color: #ffd166; }
  .movie-card .price { font-size: 1.4rem; font-weight: bold; color: #06d6a0; margin-bottom: 6px; }
  .movie-card .seats { color: #bbb; font-size: 0.9rem; margin-bottom: 15px; }
  .movie-card button {
    width: 100%; padding: 10px; border: none; border-radius: 8px;
    background: linear-gradient(90deg, #ef476f, #ffd166);
    color: #111; font-weight: bold; cursor: pointer;
    transition: opacity 0.2s;
  }
  .movie-card button:hover { opacity: 0.85; }
  .movie-card button:disabled { background: #555; color: #999; cursor: not-allowed; }
  .section-title {
    font-size: 1.5rem; margin-bottom: 15px; color: #ffd166;
    border-left: 4px solid #ef476f; padding-left: 12px;
  }
  table {
    width: 100%; border-collapse: collapse;
    background: rgba(255,255,255,0.05);
    border-radius: 12px; overflow: hidden;
  }
  th, td {
    padding: 12px 15px; text-align: left;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }
  th { background: rgba(239,71,111,0.25); color: #ffd166; font-weight: 600; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: rgba(255,255,255,0.04); }
  .empty { text-align: center; padding: 30px; color: #888; font-style: italic; }

  .modal-overlay {
    display: none; position: fixed; inset: 0;
    background: rgba(0,0,0,0.7);
    justify-content: center; align-items: center; z-index: 100;
  }
  .modal-overlay.active { display: flex; }
  .modal {
    background: #2b2b45; padding: 30px; border-radius: 14px;
    width: 90%; max-width: 400px;
    border: 1px solid rgba(255,255,255,0.1);
  }
  .modal h2 { margin-bottom: 20px; color: #ffd166; font-size: 1.3rem; }
  .modal label { display: block; margin-bottom: 6px; font-size: 0.9rem; color: #ccc; }
  .modal input {
    width: 100%; padding: 10px; border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.05);
    color: #fff; margin-bottom: 15px; font-size: 1rem;
  }
  .modal input:focus { outline: none; border-color: #ef476f; }
  .modal-buttons { display: flex; gap: 10px; margin-top: 10px; }
  .btn {
    flex: 1; padding: 11px; border: none; border-radius: 8px;
    font-weight: bold; cursor: pointer; font-size: 1rem;
  }
  .btn-primary { background: linear-gradient(90deg, #06d6a0, #118ab2); color: #fff; }
  .btn-secondary { background: rgba(255,255,255,0.1); color: #ccc; }
  .btn:hover { opacity: 0.85; }

  .toast {
    position: fixed; bottom: 30px; right: 30px;
    background: #06d6a0; color: #111;
    padding: 14px 22px; border-radius: 10px;
    font-weight: bold; box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    opacity: 0; transform: translateY(20px);
    transition: all 0.3s; z-index: 200;
  }
  .toast.error { background: #ef476f; color: #fff; }
  .toast.show { opacity: 1; transform: translateY(0); }
</style>
</head>
<body>
<div class="container">
  <h1>🎬 Movie Ticket Booking</h1>
  <p class="subtitle">Pick a movie, book your seats, enjoy the show!</p>

  <h2 class="section-title">Now Showing</h2>
  <div class="grid" id="movieGrid"></div>

  <h2 class="section-title">Your Bookings</h2>
  <div id="bookingsContainer"></div>
</div>

<div class="modal-overlay" id="modalOverlay">
  <div class="modal">
    <h2 id="modalTitle">Book Tickets</h2>
    <input type="hidden" id="movieId" />
    <label for="customerName">Your Name</label>
    <input type="text" id="customerName" placeholder="e.g. Alice" />
    <label for="ticketCount">Number of Tickets</label>
    <input type="number" id="ticketCount" min="1" value="1" />
    <div class="modal-buttons">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="confirmBooking()">Confirm</button>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
async function loadMovies() {
  const res = await fetch("/api/movies");
  const movies = await res.json();
  const grid = document.getElementById("movieGrid");
  grid.innerHTML = "";
  movies.forEach(m => {
    const disabled = m.seats === 0 ? "disabled" : "";
    grid.innerHTML += `
      <div class="movie-card">
        <h3>${m.name}</h3>
        <div class="price">₹${m.price}</div>
        <div class="seats">${m.seats} seats available</div>
        <button ${disabled} onclick="openModal(${m.id}, '${m.name}', ${m.seats})">
          ${m.seats === 0 ? "Sold Out" : "Book Now"}
        </button>
      </div>`;
  });
}

async function loadBookings() {
  const res = await fetch("/api/bookings");
  const bookings = await res.json();
  const c = document.getElementById("bookingsContainer");
  if (bookings.length === 0) {
    c.innerHTML = `<div class="empty">📭 No bookings yet.</div>`;
    return;
  }
  let html = `<table><thead><tr>
    <th>#</th><th>Customer</th><th>Movie</th><th>Tickets</th><th>Total</th>
  </tr></thead><tbody>`;
  bookings.forEach((b, i) => {
    html += `<tr>
      <td>${i + 1}</td><td>${b.customer}</td><td>${b.movie}</td>
      <td>${b.tickets}</td><td>₹${b.total}</td>
    </tr>`;
  });
  html += `</tbody></table>`;
  c.innerHTML = html;
}

function openModal(id, name, seats) {
  document.getElementById("movieId").value = id;
  document.getElementById("modalTitle").innerText = `Book: ${name}`;
  document.getElementById("customerName").value = "";
  document.getElementById("ticketCount").value = 1;
  document.getElementById("ticketCount").max = seats;
  document.getElementById("modalOverlay").classList.add("active");
}

function closeModal() {
  document.getElementById("modalOverlay").classList.remove("active");
}

async function confirmBooking() {
  const movie_id = parseInt(document.getElementById("movieId").value);
  const customer = document.getElementById("customerName").value.trim() || "Guest";
  const tickets = parseInt(document.getElementById("ticketCount").value);

  if (!tickets || tickets < 1) {
    showToast("❌ Enter a valid ticket count", true);
    return;
  }

  const res = await fetch("/api/book", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ movie_id, customer, tickets })
  });

  const data = await res.json();

  if (!res.ok) {
    showToast("❌ " + (data.detail || "Booking failed"), true);
    return;
  }

  showToast(`✅ Booked ${tickets} ticket(s) for ₹${data.total}`);
  closeModal();
  loadMovies();
  loadBookings();
}

function showToast(msg, isError = false) {
  const t = document.getElementById("toast");
  t.innerText = msg;
  t.className = "toast show" + (isError ? " error" : "");
  setTimeout(() => { t.className = "toast"; }, 3000);
}

loadMovies();
loadBookings();
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_PAGE
