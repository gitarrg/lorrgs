"""Lambda Entry Point."""

import mangum

from lorrgs_api.app import create_app


app = create_app()
handler = mangum.Mangum(app)
