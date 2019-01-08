defmodule NymServer.Repo.Migrations.AutoAddCookieTimestamps do
  use Ecto.Migration

  def change do
    alter table(:session_cookies) do
      modify :inserted_at, :datetime, default: fragment("NOW()")
      modify :updated_at, :datetime, default: fragment("NOW()")
    end
  end
end
