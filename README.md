# README

This is the personal web site http://andreinicholson.com

## Installation

The project is hosted in a shared hosting environment, so the entire project
is designed with the assumption that dependencies can and will disappear or
get upgraded to an incompatible version overnight. This is why the `vendor`
directory exists.

The shared hosting environment also means editing the Apache virtual host
configuration is out of the question. So some static files such as
`robots.txt` or `sitemap.xml` must be served by Django. The more efficient
method would be to create an alias to the direct file in Apache but that
isn't an option.

The project is nearly self-contained.

1. Clone repo outside of web-accessible location.
2. Ensure that Django is installed in a directory named `django` one level
   below this project.
3. Create an alias in htdocs of the `fcgi` directory and let `.htaccess`
   take care of the rest.
4. Run `manage.py collectstatic` and
   `manage.py assets build --parse-templates` to take care of building CSS and
   image files.

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
