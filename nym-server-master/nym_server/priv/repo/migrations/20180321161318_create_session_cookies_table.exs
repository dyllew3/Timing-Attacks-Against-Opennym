defmodule NymServer.Repo.Migrations.CreateSessionCookiesTable do
  use Ecto.Migration

  def change do
    create table(:session_cookies) do
      add :domain, :string
      add :cookies, :string
      add :nym_id, references(:nyms)

      timestamps()
    end
  end
end
