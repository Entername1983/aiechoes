import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
  Transition,
} from "@headlessui/react";
import { CheckIcon, ChevronDownIcon } from "@heroicons/react/20/solid";
import React, { Fragment, type Ref, useState } from "react";

export interface IDropdownItems {
  label: string;
  id: number;
  onClick?: () => void;
  href?: string;
  icon?: React.ReactNode;
}

interface DropdownProps {
  options: IDropdownItems[];
  label?: string;
  dropdownRef?: Ref<HTMLInputElement>;
  onChange: (value: { id: number; label: string }) => void;
  name?: string;
}

const Dropdown: React.FC<DropdownProps> = ({
  dropdownRef,
  label,
  options = [],
  onChange,
  name = "name?",
}) => {
  const [query, setQuery] = useState("");
  const [value, setValue] = useState<{ id: number; label: string }>(options[0]);
  // returns the options that match the query using regex
  const filteredOptions =
    query === ""
      ? options
      : options?.filter((option) =>
          option.label
            .toLowerCase()
            .replace(/\s+/g, "")
            .includes(query.toLowerCase().replace(/\s+/g, ""))
        );
  console.log("Filtered Options", filteredOptions);
  return (
    <div className="w-full">
      {/* Label */}
      {label != null && <p className={`top-2text-[20px] `}>{label}</p>}

      <Combobox value={value} onChange={onChange}>
        <div className="relative">
          {/* The Input and The dropdown button */}
          <div
            className={`relative w-full cursor-default overflow-hidden rounded-[18px] bg-transparent text-left  focus:outline-none  sm:text-sm`}
          >
            {/* Input */}
            <ComboboxInput
              ref={dropdownRef}
              className={"w-full p-2 pl-4 pr-10 text-black"}
              displayValue={(option: { value: number; label: string }) =>
                option.label
              }
              name={name}
              onChange={(event) => {
                setQuery(event.target.value);
              }}
            />

            {/* Button */}
            <ComboboxButton className="absolute inset-y-0 right-0 flex items-center pr-2">
              <ChevronDownIcon
                className={`dark:text-aquamarine size-[35px] text-black`}
                aria-hidden="true"
              />
            </ComboboxButton>
          </div>

          {/* This is the dropdown Body, uses the Transition from headless UI for a simple animated transition */}
          <Transition
            as={Fragment}
            leave="transition ease-in duration-100"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
            afterLeave={() => {
              setQuery("");
            }}
          >
            {/* Here Goes the options */}
            <ComboboxOptions className="absolute z-[999] mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm">
              {/* If there is a query and no results returns Nothing Found */}
              {filteredOptions != null &&
              filteredOptions.length === 0 &&
              query !== "" ? (
                <div className="relative cursor-default select-none px-4 py-2 text-gray-700">
                  Nothing found.
                </div>
              ) : (
                //   If there is a query return the matching options
                filteredOptions?.map((option) => (
                  //   this is the option component
                  <ComboboxOption
                    key={option.id}
                    className={({ focus }) =>
                      `relative cursor-default select-none py-2 pl-10 pr-4 ${
                        focus ? "bg-aquamarine text-gray-900" : "text-gray-900"
                      }`
                    }
                    value={option}
                    onChange={() => {
                      if (onChange != null) {
                        onChange(option);
                      }
                    }}
                  >
                    {/* this is a render props patterncheck https://javascriptpatterns.vercel.app/patterns/react-patterns/render-props
                     */}
                    {({ selected, focus }) => (
                      <>
                        <span
                          className={`block truncate ${
                            selected ? "font-medium" : "font-normal"
                          }`}
                        >
                          {option.label}
                        </span>

                        {/* Here renders a check-icon only when an option is selected */}
                        {selected ? (
                          <span
                            className={`absolute inset-y-0 left-0 flex items-center pl-3 ${
                              focus ? "text-gray-900" : "text-blaze-orange"
                            }`}
                          >
                            <CheckIcon className="size-5" aria-hidden="true" />
                          </span>
                        ) : null}
                      </>
                    )}
                  </ComboboxOption>
                ))
              )}
            </ComboboxOptions>
          </Transition>
        </div>
      </Combobox>
    </div>
  );
};
export { Dropdown };
