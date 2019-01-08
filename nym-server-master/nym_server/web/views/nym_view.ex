defmodule NymServer.NymView do
    use NymServer.Web, :view

    def render("index.json", %{nyms: nyms}) do
        %{
            nyms: Enum.map(nyms, &nym_json/1)
        }
    end

    def render("show.json", %{nym: nym}) do
        nym_json(nym)
    end

    def render("version_index.json", %{clustering_version: clustering_version}) do
      %{
        nym: %{
          version: clustering_version
        }
      }
    end

    def nym_json(nym) do
        %{
          nym: nym
        }
    end
end
