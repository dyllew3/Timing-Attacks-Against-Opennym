defmodule NymServer.SessionCookiesController do
  use NymServer.Web, :controller

  alias NymServer.{Nym, Rule, SessionCookies}
  alias Ecto.NoResultsError

  import NymServer.Utils

  # Given a nym ID, get the cookies for it's top domains
  def index(conn, %{"nym_id" => nym_id}) do
    case Repo.get(Nym, nym_id) do
      nil -> error_response(conn)
      nym ->
        try do
          top_cookies = nym.top_domains
                      |> Enum.map(fn(domain) -> get_domain_cookies(nym_id, domain) end)
          render(conn, "index.json", cookies: top_cookies)
        rescue
          ArgumentError -> error_response(conn, :bad_request)
          NoResultsError -> error_response(conn, :not_found)
        end
    end
  end

  # Get the session cookies for a single website given a nym id and domain
  def show(conn, %{"nym_id" => nym_id, "domain" => domain}) do
    try do
      cookies = get_domain_cookies(nym_id, domain)
      render(conn, "show.json", cookie: cookies)
    rescue
      NoResultsError ->
        case {Repo.get(Nym, nym_id), Repo.get_by(Rule, [domain: domain])} do
          {nil, _} -> error_response(conn, :bad_request)
          {_, nil} -> error_response(conn, :bad_request)
          _        -> error_response(conn, :not_found)
        end
    end
  end

  # Get the timestamp for when a cookie was updated given a nym id and domain
  def show_issued(conn, %{"nym_id" => nym_id, "domain" => domain}) do
    try do
      cookies = get_domain_cookies(nym_id, domain)
      render(conn, "show_issued.json", timestamp: cookies.updated_at)
    rescue
      NoResultsError ->
        case {Repo.get(Nym, nym_id), Repo.get_by(Rule, [domain: domain])} do
          {nil, _} -> error_response(conn, :bad_request)
          {_, nil} -> error_response(conn, :bad_request)
          _        -> error_response(conn, :not_found)
        end
    end
  end

  # Given a nym ID and domain, retrieve cookies
  defp get_domain_cookies(nym_id, domain) do
    Repo.get_by!(SessionCookies, [nym_id: nym_id, domain: domain])
  end

end
