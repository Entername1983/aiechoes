import {
  Dialog,
  DialogPanel,
  Transition,
  TransitionChild,
} from "@headlessui/react";
import { XMarkIcon } from "@heroicons/react/20/solid";
import React, { Fragment } from "react";

interface ModalWrapperProps {
  isOpen: boolean;
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
  children: React.ReactNode;
  bgColor?: string;
}
const ModalWrapper: React.FC<ModalWrapperProps> = ({
  setIsOpen,
  isOpen,
  children,
  bgColor,
}) => {
  const bgColorClass = bgColor ?? "dark:bg-offBlack bg-ghostWhite";

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog
        as={"div"}
        className={
          "fixed inset-0 z-[500] flex h-screen w-full  items-center justify-center overflow-y-auto "
        }
        open={isOpen}
        onClose={() => {
          setIsOpen(false);
        }}
      >
        <TransitionChild
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black/80" />
        </TransitionChild>
        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex h-full items-center justify-center text-center sm:p-4">
            <TransitionChild
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <DialogPanel
                className={`relative flex h-full flex-col items-center justify-between rounded-[18px] ${bgColorClass} sm:h-auto sm:flex-row sm:justify-center`}
              >
                <XMarkIcon
                  onClick={() => {
                    setIsOpen(false);
                  }}
                  className={
                    "hover:fill-tolopea absolute right-[20px] top-[20px] z-[9999]  size-[14px] cursor-pointer fill-gray-500 hover:text-white hover:dark:fill-white sm:block"
                  }
                />
                <div className="text-tolopea mx-auto flex h-screen w-screen items-center justify-center dark:text-white sm:size-full">
                  {children}
                </div>
                <button
                  onClick={() => {
                    setIsOpen(false);
                  }}
                  className="bg-mariana-blue mb-4 flex size-11 items-center justify-center rounded-full text-white sm:hidden"
                >
                  <XMarkIcon className="size-8" />
                </button>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
};
export { ModalWrapper };
