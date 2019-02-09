defmodule NymServer.RuleController do
  use NymServer.Web, :controller
  alias NymServer.{Rule, NymMetadata, Nym}
  alias Ecto.NoResultsError

  import NymServer.Utils

  # Returns a list of domains supported by OpenNym
  def supported_index(conn, _params) do
    case Repo.all Rule do
      []    -> conn
               |> error_response(:internal_server_error)
      rules -> domains = get_domains(rules)
               conn
               |> register_before_send(&pad_packet(&1))
               #|> assign(:domains, domains)
               |> send_resp(200, Poison.encode! %{ supportList: domains })
               #|> render("supported_index.json")
    end
  end

  # Returns the version of list of domains supported by OpenNym
  def supported_version_index(conn, _params) do
    case Repo.one(NymMetadata) do
      nil -> conn
             |> error_response(:internal_server_error)
      meta -> conn
              |> assign(:support_list_version, meta.support_list_version)
              |> render("supported_version_index.json")
    end
  end

  # Get rules for a given nym's top domains
  def nym_rules_show(conn, %{"nym_id" => nym_id}) do
    top_domains =
      case Repo.get(Nym, nym_id) do
        nil -> {:error, :not_found}
        nym -> nym.top_domains
      end

    case top_domains do
      {:error, reason} -> # Failed to retrieve Nym, return 404
         conn
         |> put_status(reason)
         |> text("")
      domains -> # Try get rules given domains and send back as response
        try do
          conn
          |> assign(:rules, Enum.map(domains, &get_rule/1))
          |> render("nym_rules_show.json")
        rescue
          NoResultsError -> # Failed to get rule for one of the domains, send 500
            conn
            |> error_response(:internal_server_error)
        end
    end
  end

  # Get rule given a domain
  def domain_rule_show(conn, %{"domain" => domain}) do
    case Repo.get_by(Rule, [domain: domain]) do
      nil  -> conn
              |> error_response(:bad_request)
      rule -> conn
              |> assign(:rule, rule)
              |> render("domain_rule_show.json")
    end
  end

  # Get the timestamp a rule was updated, given a domain
  def rule_issued_show(conn, %{"domain" => domain}) do
    case Repo.get_by(Rule, [domain: domain]) do
      nil  -> conn
              |> error_response(:not_found)
      rule -> conn
              |> assign(:timestamp, rule.updated_at)
              |> render("rule_issued_show.json")
    end
  end

  # Takes a list of rule objects and returns just the domains
  defp get_domains([]), do: []
  defp get_domains([h|t]), do: [h.domain | get_domains(t)]

  # Given a domain, get a rule object
  defp get_rule(domain) do
    Repo.get_by(Rule, [domain: domain])
  end
end
