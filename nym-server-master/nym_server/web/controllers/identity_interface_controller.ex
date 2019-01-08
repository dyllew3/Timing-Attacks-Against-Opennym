defmodule NymServer.IdentityInterfaceController do
    use NymServer.Web, :controller
    require Logger

    import Ecto.Query, only: [from: 2]
    import NymServer.Utils

    alias NymServer.{Nym, Rating, NymMetadata}

    def domain_index(conn, params) do
        query =
            case params do
                %{"domain" => domain, "timestamp" => timestamp} ->
                    query = from r in Rating, where: r.domain == ^domain and r.updated_at > ^timestamp, select: r
                    {:timestamp, Repo.all(query)}
                %{"domain" => domain} -> 
                    query = from r in Rating, where: r.domain == ^domain, select: r
                    {:no_timestamp, Repo.all(query)}
            end
        
        Logger.debug inspect(query)
        case query do
            {:no_timestamp, []} -> error_response(conn, :not_found)
            {:timestamp, []} -> error_response(conn, :not_modified)
            {_, ratings} -> render(conn, "domain_index.json", ratings: ratings)
        end
    end

    def nym_index(conn, params) do
        query =
            case params do
                %{"domain" => domain, "nym_id" => nym_id, "timestamp" => timestamp} ->
                    query = from r in Rating, where: r.domain == ^domain and r.nym_id == ^nym_id and r.updated_at > ^timestamp, select: r
                    {:timestamp, Repo.all(query)}
                %{"domain" => domain, "nym_id" => nym_id} -> 
                    query = from r in Rating, where: r.domain == ^domain and r.nym_id == ^nym_id, select: r
                    {:no_timestamp, Repo.all(query)}
            end
        
        case query do
            {:no_timestamp, []} -> error_response(conn, :not_found)
            {:timestamp, []} -> error_response(conn, :not_modified)
            {_, ratings} -> render(conn, "domain_index.json", ratings: ratings)
        end
    end

    def map_username(conn, %{"domain" => domain, "username" => username}) do

    end

end

