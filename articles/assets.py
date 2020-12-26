from django_assets import Bundle, register

public_no_code = Bundle(
    "newcss.css",
    "public.css",
    filters="rcssmin",
    output="public_bundled.css",
)
public_with_code = Bundle(
    "newcss.css",
    "codehilite.css",
    "public.css",
    filters="rcssmin",
    output="public_code_bundled.css",
)
register("public_no_code", public_no_code)
register("public_with_code", public_with_code)