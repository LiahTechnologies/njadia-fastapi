

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        reload=True,
        # debug=True,
        app="main:app",
        # host="192.168.100.74" 
    )