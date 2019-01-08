defmodule NymServer.Repo.Migrations.ChangeCookiesToText do
  use Ecto.Migration

  def change do
    alter table(:session_cookies) do
        modify :cookies, :text
    end
  end
end
