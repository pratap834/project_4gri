"""
Government Schemes API
Provides endpoints for listing, filtering, and searching government agricultural schemes
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from datetime import datetime

app = FastAPI(title="Government Schemes API")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load schemes data
schemes_data = {}
schemes_file = "government_schemes_data.json"

def load_schemes():
    global schemes_data
    try:
        with open(schemes_file, 'r', encoding='utf-8') as f:
            schemes_data = json.load(f)
        print(f"✓ Loaded {len(schemes_data.get('schemes', []))} government schemes")
    except FileNotFoundError:
        print(f"! Schemes data file not found: {schemes_file}")
        schemes_data = {"schemes": [], "categories": [], "states": []}
    except Exception as e:
        print(f"Error loading schemes data: {e}")
        schemes_data = {"schemes": [], "categories": [], "states": []}

# Load data on startup
@app.on_event("startup")
async def startup_event():
    load_schemes()

# Response models
class SchemeResponse(BaseModel):
    id: str
    name: str
    category: str
    description: str
    benefits: str
    eligibility: List[str]
    documents_required: List[str]
    how_to_apply: str
    state: str
    department: str
    official_website: str
    helpline: str
    last_updated: str

class SchemesListResponse(BaseModel):
    total: int
    schemes: List[SchemeResponse]
    categories: List[str]
    states: List[str]

class FilterOptions(BaseModel):
    categories: List[str]
    states: List[str]

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Government Schemes API",
        "version": "1.0.0",
        "total_schemes": len(schemes_data.get("schemes", [])),
        "endpoints": {
            "schemes": "/api/schemes",
            "scheme_detail": "/api/schemes/{scheme_id}",
            "filter_options": "/api/schemes/filters",
            "search": "/api/schemes/search"
        }
    }

@app.get("/api/schemes/search")
async def search_schemes(
    q: str = Query(..., description="Search query"),
    state: Optional[str] = Query(None, description="Filter by state"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """
    Search schemes by name, description, or benefits
    """
    schemes = schemes_data.get("schemes", [])
    query_lower = q.lower()
    
    # Search in name, description, and benefits
    matching_schemes = []
    for scheme in schemes:
        if (query_lower in scheme["name"].lower() or
            query_lower in scheme["description"].lower() or
            query_lower in scheme["benefits"].lower() or
            any(query_lower in doc.lower() for doc in scheme.get("eligibility", [])) or
            query_lower in scheme["category"].lower()):
            
            # Apply additional filters
            if state and state != "All":
                if scheme["state"] != state and scheme["state"] != "All India":
                    continue
            
            if category and category != "All":
                if scheme["category"] != category:
                    continue
            
            matching_schemes.append(scheme)
    
    return {
        "total": len(matching_schemes),
        "query": q,
        "schemes": matching_schemes,
        "categories": schemes_data.get("categories", []),
        "states": schemes_data.get("states", [])
    }

@app.get("/api/schemes/filters", response_model=FilterOptions)
async def get_filter_options():
    """
    Get available filter options (categories and states)
    """
    return {
        "categories": schemes_data.get("categories", []),
        "states": schemes_data.get("states", [])
    }

@app.get("/api/schemes/stats")
async def get_schemes_statistics():
    """
    Get statistics about available schemes
    """
    schemes = schemes_data.get("schemes", [])
    categories = schemes_data.get("categories", [])
    states = schemes_data.get("states", [])
    
    # Count schemes by category
    category_counts = {}
    for category in categories:
        count = len([s for s in schemes if s["category"] == category])
        category_counts[category] = count
    
    # Count schemes by state
    state_counts = {}
    for state in states:
        if state == "All India":
            count = len([s for s in schemes if s["state"] == "All India"])
        else:
            count = len([s for s in schemes if s["state"] == state])
        state_counts[state] = count
    
    return {
        "total_schemes": len(schemes),
        "total_categories": len(categories),
        "total_states": len(states),
        "schemes_by_category": category_counts,
        "schemes_by_state": state_counts,
        "last_updated": max([s.get("last_updated", "2024-01-01") for s in schemes]) if schemes else None
    }

@app.get("/api/schemes/category/{category}")
async def get_schemes_by_category(category: str):
    """
    Get all schemes in a specific category
    """
    schemes = schemes_data.get("schemes", [])
    category_schemes = [s for s in schemes if s["category"].lower() == category.lower()]
    
    if not category_schemes:
        raise HTTPException(status_code=404, detail=f"No schemes found in category '{category}'")
    
    return {
        "category": category,
        "total": len(category_schemes),
        "schemes": category_schemes
    }

@app.get("/api/schemes/state/{state}")
async def get_schemes_by_state(state: str):
    """
    Get all schemes available for a specific state
    """
    schemes = schemes_data.get("schemes", [])
    state_schemes = [s for s in schemes if s["state"] == state or s["state"] == "All India"]
    
    if not state_schemes:
        raise HTTPException(status_code=404, detail=f"No schemes found for state '{state}'")
    
    return {
        "state": state,
        "total": len(state_schemes),
        "schemes": state_schemes
    }

@app.get("/api/schemes", response_model=SchemesListResponse)
async def get_schemes(
    state: Optional[str] = Query(None, description="Filter by state"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: Optional[int] = Query(None, description="Limit number of results"),
    offset: Optional[int] = Query(0, description="Offset for pagination")
):
    """
    Get list of government schemes with optional filtering
    """
    schemes = schemes_data.get("schemes", [])
    
    # Apply filters
    filtered_schemes = schemes
    
    if state and state != "All":
        filtered_schemes = [s for s in filtered_schemes if s["state"] == state or s["state"] == "All India"]
    
    if category and category != "All":
        filtered_schemes = [s for s in filtered_schemes if s["category"] == category]
    
    # Apply pagination
    total = len(filtered_schemes)
    if limit:
        filtered_schemes = filtered_schemes[offset:offset+limit]
    else:
        filtered_schemes = filtered_schemes[offset:]
    
    return {
        "total": total,
        "schemes": filtered_schemes,
        "categories": schemes_data.get("categories", []),
        "states": schemes_data.get("states", [])
    }

@app.get("/api/schemes/{scheme_id}", response_model=SchemeResponse)
async def get_scheme_by_id(scheme_id: str):
    """
    Get detailed information about a specific scheme
    """
    schemes = schemes_data.get("schemes", [])
    
    for scheme in schemes:
        if scheme["id"] == scheme_id:
            return scheme
    
    raise HTTPException(status_code=404, detail=f"Scheme with ID '{scheme_id}' not found")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "schemes_loaded": len(schemes_data.get("schemes", [])),
        "categories": len(schemes_data.get("categories", [])),
        "states": len(schemes_data.get("states", []))
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Government Schemes API on port 8003...")
    uvicorn.run(app, host="0.0.0.0", port=8003)
