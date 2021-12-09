import pandas as pd

df = pd.read_csv("input.txt", sep=" ", header=None, dtype=str)

def find_rating(df: pd.DataFrame, target_rating: str) -> str:
    print(f"---Looking for rating: {target_rating}---")
    match target_rating:
        case "o_2":
            #Find o_2 generator rating by filtering for remaining values equal to most bits in selection col
            for col in range(0, len(df[0][0])):
                most_bits_char = ""
                true_bit_count = 0
                print(f"Checking col: {col}, of {len(df[0])} items.")
                for obs in df[0]:
                    print(obs)
                    if obs[col] == "1":
                        true_bit_count += 1
                print(f"True bits: {true_bit_count}")
                most_bits_char = "1" if true_bit_count >= len(df[0]) / 2 else "0"
                df = df[df[0].str[col] == most_bits_char]
                if len(df) == 0:
                    print(f"Rating {target_rating} was not found!")
                    break
                if len(df) == 1:
                    #Found the target rating
                    break


                print(f"Kept {most_bits_char}'s")
                print(df[0])
            return df[0].head(1).values[0]
        case "co_2": 
            #Find co_2 generator rating by filtering for remaining values equal to least bits in selection col
            for col in range(0, len(df[0][0])):
                least_bits_char = ""
                true_bit_count = 0
                print(f"Checking col: {col}, of {len(df[0])} items.")
                for obs in df[0]:
                    print(obs)
                    if obs[col] == "1":
                        true_bit_count += 1
                print(f"True bits: {true_bit_count}")
                least_bits_char = "0" if true_bit_count >= len(df[0]) / 2 else "1"
                df = df[df[0].str[col] == least_bits_char]
                if len(df) == 0:
                    print(f"Rating {target_rating} was not found!")
                    break
                if len(df) == 1:
                    #Found the target rating
                    break


                print(f"Kept {least_bits_char}'s")
                print(df[0])
            return df[0].head(1).values[0]
        case _:
            print(f"Target rating {target_rating} is not handled.")

#Determine power consumption
true_bit_counts = [0] * len(df[0][0])
for obs in df[0]:
    print(obs)
    for i in range(0, len(obs)):
        if obs[i] == "1":
            true_bit_counts[i] += 1

print(f"Num observations = {len(df)}")
gamma = "".join([str(int(x > (len(df)/2))) for x in true_bit_counts])
epsilon = gamma.replace("1", "2").replace("0", "1").replace("2", "0")
o2_generator_rating = int(find_rating(df, "o_2"),2)
co2_scrubber_rating = int(find_rating(df, "co_2"), 2)


print(f"Bit counts: {true_bit_counts}")
print(f"Gamma(binary): {gamma}")
print(f"Epsilon(binary): {epsilon}")
print(f"Power consumption = {int(gamma,2) * int(epsilon, 2)} = Gamma: {int(gamma,2)} * Epsilon: {int(epsilon, 2)}")
print()
# print(f"Life support rating = unknown = O_2 Gen Rating: {o2_generator_rating} * CO_2 Scrubing: {co2_scrubber_rating}")
print(f"Life support rating = {o2_generator_rating * co2_scrubber_rating} = O_2 Gen Rating: {o2_generator_rating} * CO_2 Scrubing: {co2_scrubber_rating}")