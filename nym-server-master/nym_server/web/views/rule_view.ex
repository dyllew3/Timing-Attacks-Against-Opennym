defmodule NymServer.RuleView do
  use NymServer.Web, :view

  def render("supported_index.json", %{domains: domains}) do
    %{
      supportList: domains
    }
  end

  def render("supported_version_index.json", %{support_list_version: support_list_version}) do
    %{
      version: support_list_version
    }
  end

  def render("nym_rules_show.json", %{rules: rules}) do
    %{
      rules: Enum.map(rules, &render_rule/1)
    }
  end

  def render("domain_rule_show.json", %{rule: rule}) do
    render_rule(rule)
  end

  def render("rule_issued_show.json", %{timestamp: timestamp}) do
    %{
      domainRule: %{
        timestamp: timestamp
      }
    }
  end

  defp render_rule(rule) do
    %{
      domainRule: %{
        domain: rule.domain,
        timestamp: rule.updated_at,
        rule: %{
          endpoint: rule.endpoint,
          regex: rule.rule
        }
      }
    }
  end
end
