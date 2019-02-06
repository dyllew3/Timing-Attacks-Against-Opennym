defmodule NymServer.Utils do
  alias Phoenix.Controller, as: PCon
  alias Plug.Conn, as: PC
  alias Code
  alias Integer

  def pad_packet(conn) do
    base_size = 204 + byte_size("padding-len") + byte_size(conn.resp_body)
    max_size = 15202
    padding_size = max_size - base_size
    padding = for _ <- 1 .. (padding_size), do: '0'
    padding_size_string = cond do

      padding_size >= 10000 ->
        Integer.to_string(padding_size)


      padding_size >= 1000 ->
        Enum.join(["0",Integer.to_string(padding_size)], "")

      padding_size < 1000 and padding_size >= 100 ->
        Enum.join(["00",Integer.to_string(padding_size)], "")

      padding_size < 100 and padding_size >= 10 ->
        Enum.join(["000",Integer.to_string(padding_size)], "")

      padding_size < 10 ->
        Enum.join(["0000",Integer.to_string(padding_size)], "")
    end

    conn
    |> PC.resp(200, Enum.join([conn.resp_body, padding], ""))
    |> PC.put_resp_header("padding-len", padding_size_string)
    |> PC.update_resp_header("content-length", "15202", &(&1 <> "; content-length=15202"))
  end

  def error_response(conn, reason \\ :bad_request) do
    conn
    |> PC.put_status(reason)
    |> PCon.text("")
  end
end
