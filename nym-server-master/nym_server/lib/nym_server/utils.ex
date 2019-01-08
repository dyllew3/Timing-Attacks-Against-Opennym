defmodule NymServer.Utils do
  alias Phoenix.Controller, as: PCon
  alias Plug.Conn, as: PC

  def error_response(conn, reason \\ :bad_request) do
    conn
    |> PC.put_status(reason)
    |> PCon.text("")
  end
end
