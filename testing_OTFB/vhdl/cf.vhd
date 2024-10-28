library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity cf is
  generic(
    N : integer := 16;
    D : integer := 128
  );
  port(
    clk : in std_logic;
    rst : in std_logic;
    
    g   : in std_logic_vector(N-1 downto 0);
    vdel : in std_logic_vector(31 downto 0);
    dfrac : in std_logic_vector(17 downto 0);
    din   : in std_logic_vector(N-1 downto 0);
    dout  : out std_logic_vector(N-1 downto 0)
  );
end entity cf;

architecture rtl of cf is

  signal s1 : std_logic_vector(2*N-1 downto 0) := (others => '0');
  signal s2 : std_logic_vector(2*N-1 downto 0) := (others => '0');
  signal s3 : std_logic_vector(2*N-1 downto 0) := (others => '0');

  signal s2_temp : std_logic_vector(2*N-1 downto 0) := (others => '0');
  signal s2_vfd  : std_logic_vector(2*N-1 downto 0) := (others => '0');

  signal dout_reg : std_logic_vector(2*N-1 downto 0) := (others => '0');
  
  component var_delay
    generic (
      N : integer;
      D : integer
    );
    port(
      clk : in std_logic;
      rst : in std_logic;
      del : in std_logic_vector(N-1 downto 0);
      din : in std_logic_vector(N-1 downto 0);
      dout : out std_logic_vector(N-1 downto 0)
    );
  end component;

begin

  -- register the inputs and outputs
  process(clk)
  begin
    if rising_edge(clk) then
      dout <= dout_reg(N-1 downto 0);
    end if;
  end process;

  -- adder after input
  process(clk)
  begin
    if rising_edge(clk) then
      s1 <= std_logic_vector(signed(din)+signed(s3));
    end if;
  end process;

  -- multiply by 1-a
  process(clk)
  begin
    if rising_edge(clk) then
      s2_temp <= std_logic_vector(shift_right(signed(s2),to_integer(signed(g))));
      s3 <= std_logic_vector(signed(s2) - signed(s2_temp));
    end if;
  end process;

  -- multiply by a into the output register
  process(clk)
  begin
    if rising_edge(clk) then
      dout_reg <= std_logic_vector(shift_right(signed(s1),to_integer(signed(g))));
    end if;
  end process;
  
  -- delay registers
  int_delay : var_delay
  generic map(
    N => 2*N,
    D => D-1 --was 11 with vfd
  )
  port map(
    clk => clk,
    rst => rst,
    del => vdel,
    din => s1,
    dout => s2
  );

end architecture rtl;

