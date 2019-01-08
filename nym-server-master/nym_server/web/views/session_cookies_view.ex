defmodule NymServer.SessionCookiesView do
  use NymServer.Web, :view

  def render("index.json", %{cookies: cookies}) do
    %{
      cookies: Enum.map(cookies, &render_cookie/1)
    }
  end

  def render("show.json", %{cookie: cookie}) do
    render_cookie(cookie)
  end

  def render("show_issued.json", %{timestamp: timestamp}) do
    %{
      session: %{
        issued: timestamp
      }
    }
  end

  defp render_cookie(cookie) do
    %{
      session: %{
        domain: cookie.domain,
        issued: cookie.updated_at,
        cookies: Poison.decode! cookie.cookies
      }
    }
  end
end
