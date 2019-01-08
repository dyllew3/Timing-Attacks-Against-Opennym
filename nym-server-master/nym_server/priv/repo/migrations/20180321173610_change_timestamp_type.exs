defmodule NymServer.Repo.Migrations.ChangeTimestampType do
  use Ecto.Migration

  def change do
    alter table(:session_cookies) do
      modify :inserted_at, :utc_datetime, default: fragment("NOW()")
      modify :updated_at, :utc_datetime, default: fragment("NOW()")
    end
  end
end
